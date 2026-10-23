"""Run the frozen-source audit suites. Python/Maven are maintenance dependencies only."""
from __future__ import annotations
import concurrent.futures
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
JAVA_HOME = Path(subprocess.run(['/usr/libexec/java_home', '-v', '1.8'], capture_output=True, text=True, check=True).stdout.strip())
ENV = os.environ.copy()
ENV.update(JAVA_HOME=str(JAVA_HOME), PATH=str(JAVA_HOME/'bin')+os.pathsep+ENV['PATH'],
           GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', PYTHONDONTWRITEBYTECODE='1')
SCRIPTS = ROOT/'skills/uaw-sdd-ai-coding/scripts'
JAR = SCRIPTS/'runtime/sdd2-control.jar'


def run(name, command, cwd=ROOT, env=ENV):
    started = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
    start = time.monotonic()
    p = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=1800)
    content = p.stdout+p.stderr
    (HERE/(name+'.log')).write_text(content)
    result = {'name': name, 'started_at': started, 'seconds': round(time.monotonic()-start,3),
              'exit_code': p.returncode, 'command': [str(v) for v in command],
              'log_sha256': hashlib.sha256(content.encode()).hexdigest()}
    if name.startswith('demo-'):
        try: result['summary'] = json.loads(p.stdout)
        except ValueError: pass
    print(json.dumps({'name':name,'exit_code':p.returncode,'seconds':result['seconds']}),flush=True)
    return result


def maven_baseline():
    with tempfile.TemporaryDirectory(prefix='sdd2-audit-java-demo-') as tmp:
        source=Path(tmp)/'uaw-sdd-demo'
        shutil.copytree(ROOT/'uaw-sdd-demo',source,ignore=shutil.ignore_patterns('target','.DS_Store','__pycache__'))
        r=run('maven-baseline',['mvn','-q','test'],source)
        counts={'tests':0,'failures':0,'errors':0,'skipped':0}
        for p in source.glob('target/surefire-reports/TEST-*.xml'):
            node=ET.parse(p).getroot()
            for key in counts: counts[key]+=int(node.get(key,0))
        r['counts']=counts
        return r


def minimal_runtime():
    with tempfile.TemporaryDirectory(prefix='sdd2-audit-offline-') as tmp:
        root=Path(tmp); binary=root/'bin';binary.mkdir()
        for name,path in [('java',JAVA_HOME/'bin/java'),('git',Path(shutil.which('git')))]:
            (binary/name).symlink_to(path)
        shutil.copytree(ROOT/'skills',root/'skills',ignore=shutil.ignore_patterns('__pycache__','.DS_Store'))
        env=ENV.copy();env['PATH']=str(binary)
        return run('java8-git-only',['java','-jar',str(root/'skills/uaw-sdd-ai-coding/scripts/runtime/sdd2-control.jar'),'doctor','--repo-root',str(root)],root,env)

jobs=[('controller-and-validator',lambda:run('controller-and-validator',[sys.executable,'-B','-m','unittest','discover','-s',str(SCRIPTS/'tests'),'-p','test_*.py','-v'])),
      ('static-assets',lambda:run('static-assets',[sys.executable,'-B',str(SCRIPTS/'validate_sdd2_assets.py')])),
      ('maven-baseline',maven_baseline),('java8-git-only',minimal_runtime)]
for short, filename in [('small','demo_sdd2_small_feature.py'),('large','demo_sdd2_large_feature.py'),('mutation','demo_sdd2_mutation_mapping_feature.py')]:
    jobs.append(('demo-'+short,lambda s=short,f=filename:run('demo-'+s,[sys.executable,'-B',str(SCRIPTS/f)])))
source_paths=subprocess.run(['git','ls-files','-z','--','skills'],cwd=ROOT,capture_output=True,check=True).stdout.decode().split('\0')
source_hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in source_paths if name}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    fs={pool.submit(fn):name for name,fn in jobs}
    for f in concurrent.futures.as_completed(fs):
        try:results.append(f.result())
        except Exception as e:results.append({'name':fs[f],'exit_code':-1,'error':str(e)})
report={'recorded_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),'device':'Mac-Air',
        'baseline_commit':subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip(),
        'source_hashes':source_hashes,'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'java_home':str(JAVA_HOME),'jar_sha256':hashlib.sha256(JAR.read_bytes()).hexdigest(),'results':results}
report['source_unchanged_during_verification']=all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in source_hashes.items())
(HERE/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
raise SystemExit(0 if all(r['exit_code']==0 for r in results) and report['source_unchanged_during_verification'] else 1)
