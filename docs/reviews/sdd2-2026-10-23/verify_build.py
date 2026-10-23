"""Recompile to a temporary directory and compare every class without replacing the runtime."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib,json,subprocess,tempfile,zipfile,struct
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SOURCE=ROOT/'skills/uaw-sdd-ai-coding/scripts/Sdd2Control.java'
JAR=SOURCE.parent/'runtime/sdd2-control.jar'
java_home=Path(subprocess.run(['/usr/libexec/java_home','-v','17'],capture_output=True,text=True,check=True).stdout.strip())
with tempfile.TemporaryDirectory(prefix='sdd2-freeze-build-check-') as tmp:
    build=subprocess.run([str(java_home/'bin/javac'),'--release','8','-Xlint:all','-encoding','UTF-8','-d',tmp,str(SOURCE)],capture_output=True,text=True)
    if build.returncode:raise SystemExit(build.stderr)
    compiled={p.relative_to(tmp).as_posix():p.read_bytes() for p in Path(tmp).rglob('*.class')}
    with zipfile.ZipFile(JAR) as z:
        bundled={name:z.read(name) for name in z.namelist() if name.endswith('.class')}
    match=compiled==bundled
    majors=sorted({struct.unpack('>H',content[6:8])[0] for content in bundled.values()})
result={'recorded_at':datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),'device':'Mac-Air',
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'jar_sha256':hashlib.sha256(JAR.read_bytes()).hexdigest(),'class_count':len(compiled),
        'class_majors':majors,'class_bytes_identical':match,'compiler_exit_code':build.returncode}
(HERE/'build-consistency.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
raise SystemExit(0 if match and majors==[52] else 1)
