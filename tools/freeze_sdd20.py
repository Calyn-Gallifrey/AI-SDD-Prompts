"""Maintenance-only creation/verification of the SDD2.0 frozen package (Python standard library)."""
from __future__ import annotations
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile

TAG = 'sdd2.0-frozen-2026-10-23'
RELEASE = Path('releases/sdd2.0')
AUDIT = Path('docs/reviews/sdd2-2026-10-23')
NAMES = ('uaw-sdd-ai-coding','uaw-code-review','uaw-unit-test')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ignored(path):
    return path.name in {'.DS_Store','Thumbs.db','Desktop.ini'} or path.name.startswith('._') or '__pycache__' in path.parts


def actual_files(root):
    found=set()
    for p in (root/'skills').rglob('*'):
        if ignored(p):continue
        if p.is_symlink():raise ValueError('Frozen source contains symlink: '+str(p))
        if p.is_file():found.add(p.relative_to(root).as_posix())
    return found


def safe_path(root, name):
    path=Path(name)
    if path.is_absolute() or '..' in path.parts:raise ValueError('Unsafe manifest path')
    candidate=root/path
    candidate.resolve().relative_to(root.resolve())
    if candidate.is_symlink():raise ValueError('Frozen evidence symlink')
    return candidate


def tracked_files(root):
    rows=subprocess.run(['git','ls-files','--stage','-z','--','skills'],cwd=root,capture_output=True,check=True).stdout.decode().split('\0')
    records=[]
    for row in rows:
        if not row:continue
        metadata,name=row.split('\t',1)
        mode,_,stage=metadata.split()
        if stage!='0' or mode not in {'100644','100755'}:raise ValueError('Unsupported source entry: '+name)
        p=root/name
        if ignored(p):continue
        records.append({'path':name,'git_mode':mode,'size':p.stat().st_size,'sha256':digest(p)})
    if {r['path'] for r in records} != actual_files(root):raise ValueError('Tracked and physical Skill members differ')
    return sorted(records,key=lambda r:r['path'])


def create(root):
    target=root/RELEASE
    if (target/'manifest.json').exists() or (target/'sdd2.0-skills.zip').exists():
        raise ValueError('Frozen package already exists; never overwrite it')
    verification=json.loads((root/AUDIT/'verification.json').read_text())
    probes=json.loads((root/AUDIT/'probe-results.json').read_text())
    build=json.loads((root/AUDIT/'build-consistency.json').read_text())
    if not build.get('class_bytes_identical') or build.get('class_majors')!=[52]:
        raise ValueError('Runtime/source correspondence must pass before freeze')
    if not verification.get('source_unchanged_during_verification') or any(r['exit_code'] for r in verification['results']):
        raise ValueError('Full verification must pass before freeze')
    if any(not c['probe_completed'] or c.get('contract_violation') for c in probes['cases']):
        raise ValueError('Audit probes must pass before freeze')
    if subprocess.run(['git','show-ref','--verify','--quiet','refs/tags/'+TAG],cwd=root,capture_output=True).returncode==0:
        raise ValueError('Frozen tag already exists; never recreate this release')
    files=tracked_files(root)
    if verification['source_hashes'] != {r['path']:r['sha256'] for r in files}:
        raise ValueError('Verification is stale for these sources')
    jar='skills/uaw-sdd-ai-coding/scripts/runtime/sdd2-control.jar'
    if probes['jar_sha256'] != digest(root/jar) or build['jar_sha256'] != digest(root/jar):raise ValueError('Probe/build runtime is stale')
    if build['source_sha256'] != digest(root/'skills/uaw-sdd-ai-coding/scripts/Sdd2Control.java'):raise ValueError('Build source is stale')
    target.mkdir(parents=True,exist_ok=True)
    archive=target/'sdd2.0-skills.zip'
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for item in files:
            info=zipfile.ZipInfo(item['path'],(2026,10,23,0,0,0))
            info.create_system=3
            info.external_attr=int(item['git_mode'],8)<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,(root/item['path']).read_bytes())
    evidence=[AUDIT/'verification.json',AUDIT/'probe-results.json',AUDIT/'run_audit.py',AUDIT/'audit_probes.py',AUDIT/'build-consistency.json',AUDIT/'verify_build.py',Path('tools/freeze_sdd20.py')]
    manifest={'format_version':1,'product':'SDD2.0','controller_version':'2.0-java8.3',
              'freeze_tag':TAG,'created_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
              'source_tree_sha256':hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
              'files':files,'evidence':{p.as_posix():digest(root/p) for p in evidence},
              'package':{'path':archive.relative_to(root).as_posix(),'size':archive.stat().st_size,'sha256':digest(archive)}}
    (target/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    sums=''.join(digest(root/p)+'  '+p.as_posix()+'\n' for p in [RELEASE/'manifest.json',RELEASE/'sdd2.0-skills.zip'])
    (target/'SHA256SUMS').write_text(sums)
    return verify(root)


def verify(root):
    manifest=json.loads((root/RELEASE/'manifest.json').read_text())
    if manifest.get('freeze_tag')!=TAG or manifest.get('controller_version')!='2.0-java8.3':raise ValueError('Freeze identity mismatch')
    files=manifest['files']
    if {r['path'] for r in files} != actual_files(root):raise ValueError('Frozen Skill membership changed')
    for item in files:
        name=item['path']
        if not name.startswith('skills/') or '..' in Path(name).parts:raise ValueError('Invalid manifest path')
        p=root/name
        if digest(p)!=item['sha256'] or p.stat().st_size!=item['size']:raise ValueError('Source drift: '+name)
        if os.name!='nt':
            mode='100755' if p.stat().st_mode & 0o111 else '100644'
            if mode!=item['git_mode']:raise ValueError('Mode drift: '+name)
    calculated=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if calculated!=manifest['source_tree_sha256']:raise ValueError('Manifest source digest mismatch')
    for name,expected in manifest['evidence'].items():
        if digest(safe_path(root,name))!=expected:raise ValueError('Evidence drift: '+name)
    archive=safe_path(root,manifest['package']['path'])
    if digest(archive)!=manifest['package']['sha256']:raise ValueError('Package digest mismatch')
    with zipfile.ZipFile(archive) as z:
        if len(z.namelist())!=len(files) or set(z.namelist())!={r['path'] for r in files}:raise ValueError('Package membership mismatch')
        for item in files:
            if hashlib.sha256(z.read(item['path'])).hexdigest()!=item['sha256']:raise ValueError('Package content mismatch')
    runtime=root/'skills/uaw-sdd-ai-coding/scripts/runtime/sdd2-control.jar'
    if digest(runtime)!=runtime.with_suffix('.sha256').read_text().strip():raise ValueError('Runtime pair mismatch')
    checksum_entries={}
    for line in (root/RELEASE/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        if name in checksum_entries:raise ValueError('Duplicate release checksum')
        checksum_entries[name]=expected
        if digest(safe_path(root,name))!=expected:raise ValueError('Release checksum mismatch: '+name)
    if set(checksum_entries)!={(RELEASE/'manifest.json').as_posix(),(RELEASE/'sdd2.0-skills.zip').as_posix()}:
        raise ValueError('Incomplete release checksum list')
    return {'valid':True,'freeze_tag':TAG,'file_count':len(files),'source_tree_sha256':calculated,
            'package_sha256':manifest['package']['sha256']}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--create',action='store_true')
    args=parser.parse_args()
    try:
        print(json.dumps(create(args.root.resolve()) if args.create else verify(args.root.resolve()),ensure_ascii=False,indent=2))
    except (ValueError,OSError,KeyError,zipfile.BadZipFile) as e:
        print(json.dumps({'valid':False,'error':str(e)},ensure_ascii=False))
        raise SystemExit(1)
