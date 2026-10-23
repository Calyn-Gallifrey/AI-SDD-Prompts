"""Fault injection against copies of the package; never changes the actual frozen artifacts."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
RELEASE=Path('releases/sdd2.0')
manifest=json.loads((ROOT/RELEASE/'manifest.json').read_text())
files={item['path'] for item in manifest['files']} | set(manifest['evidence'])
files |= {(RELEASE/'manifest.json').as_posix(),(RELEASE/'SHA256SUMS').as_posix(),manifest['package']['path']}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def change_source(root):
 p=root/'skills/uaw-sdd-ai-coding/SKILL.md';p.write_text(p.read_text()+'\n篡改样本\n')
def add_source(root):(root/'skills/extra-skill').mkdir();(root/'skills/extra-skill/SKILL.md').write_text('unexpected')
def change_runtime_pair(root):(root/'skills/uaw-sdd-ai-coding/scripts/runtime/sdd2-control.sha256').write_text('0'*64+'\n')
def change_package(root):
 p=root/manifest['package']['path'];p.write_bytes(p.read_bytes()+b'changed')
def change_evidence(root):
 p=root/'docs/reviews/sdd2-2026-10-23/verification.json';p.write_text(p.read_text()+'\n')
def empty_sums(root):(root/RELEASE/'SHA256SUMS').write_text('')
def change_mode(root):
 p=root/'skills/uaw-sdd-ai-coding/SKILL.md';p.chmod(p.stat().st_mode | 0o111)
def inconsistent_package(root):
 archive=root/manifest['package']['path']
 with zipfile.ZipFile(archive) as z:items=[(i,z.read(i.filename)) for i in z.infolist()]
 with zipfile.ZipFile(archive,'w') as z:
  for i,content in items:z.writestr(i,content+b'changed' if i.filename.endswith('uaw-sdd-ai-coding/SKILL.md') else content)
 data=json.loads((root/RELEASE/'manifest.json').read_text());data['package']['sha256']=sha(archive)
 (root/RELEASE/'manifest.json').write_text(json.dumps(data))
 (root/RELEASE/'SHA256SUMS').write_text(''.join(sha(root/p)+'  '+p.as_posix()+'\n' for p in [RELEASE/'manifest.json',RELEASE/'sdd2.0-skills.zip']))

cases=[('original',None,0),('source-change',change_source,1),('extra-skill',add_source,1),
       ('runtime-checksum-change',change_runtime_pair,1),('package-change',change_package,1),
       ('evidence-change',change_evidence,1),('checksum-list-missing',empty_sums,1),
       ('package-content-with-updated-outer-checksum',inconsistent_package,1)]
if os.name!='nt':cases.append(('executable-mode-change',change_mode,1))
results=[]
for name,mutate,expected in cases:
 with tempfile.TemporaryDirectory(prefix='sdd2-freeze-check-') as tmp:
  root=Path(tmp)
  for rel in files:
   target=root/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,target)
  if mutate:mutate(root)
  p=subprocess.run([sys.executable,'-B',str(ROOT/'tools/freeze_sdd20.py'),'--root',str(root)],capture_output=True,text=True,timeout=30)
  results.append({'case':name,'expected_exit':expected,'actual_exit':p.returncode,'passed':p.returncode==expected,'output':json.loads(p.stdout)})
report={'recorded_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),'device':'Mac-Air','cases':results}
(HERE/'freeze-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':sum(r['passed'] for r in results),'total':len(results),'failures':[r for r in results if not r['passed']]},ensure_ascii=False,indent=2))
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
