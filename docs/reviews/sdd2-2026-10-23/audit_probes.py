"""SDD2.0 audit probes; all state mutations and simulated approvals use temporary repositories."""
from __future__ import annotations
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
os.environ['GIT_CONFIG_GLOBAL'] = os.devnull
os.environ['GIT_CONFIG_NOSYSTEM'] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
spec = importlib.util.spec_from_file_location('sdd_fixture', ROOT / 'skills/uaw-sdd-ai-coding/scripts/tests/test_sdd2_control.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
RESULTS = []


def command(t, *args):
    p = subprocess.run([*fixture.JAVA_CONTROL_COMMAND, args[0], '--feature-dir', str(t.feature), *args[1:]],
                       cwd=t.repo, text=True, capture_output=True, timeout=45)
    try:
        data = json.loads(p.stdout)
    except ValueError:
        data = {'error': (p.stdout + p.stderr)[:2000]}
    state = data.get('result', {})
    return {'exit_code': p.returncode, 'error': data.get('error'),
            'stage': state.get('current_stage'), 'status': state.get('stage_status'),
            'next_action': state.get('next_required_action'), 'outcome': state.get('outcome'),
            'valid': state.get('valid'), 'counts': state.get('counts'), 'result': state}


def run_case(name, fn):
    t = fixture.Sdd2ControlTest('test_doctor_is_read_only')
    try:
        t.setUp()
        detail = fn(t)
        RESULTS.append({'case': name, 'probe_completed': True, **detail})
    except Exception as e:
        RESULTS.append({'case': name, 'probe_completed': False, 'error': str(e)[:3000]})
    finally:
        if hasattr(t, 'temp'):
            t.tearDown()


def spec_gate(t):
    t._record('proposal-input', 'proposal-input.md', '# 内部规划\n')
    t._record('spec', 'spec.md', '# 需求规格\n')


def approval_probe(t, text):
    spec_gate(t)
    r = command(t, 'approve', '--stage', 'spec', '--source', 'user-message', '--approver-role', 'human',
                '--approval-text', text, '--message-id', 'audit-simulated-message')
    r.pop('result')
    return {'input': text, 'expected': 'reject', 'contract_violation': r['exit_code'] == 0, **r}


def close_probe(t):
    r = command(t, 'close', '--result', 'aborted', '--approval-text', '不同意终止，继续保留当前流程')
    r.pop('result')
    return {'input': '不同意终止，继续保留当前流程', 'expected': 'reject', 'contract_violation': r['exit_code'] == 0, **r}


def restart_probe(t):
    t._run('close', '--feature-dir', str(t.feature), '--result', 'aborted', '--approval-text', '同意终止')
    r = command(t, 'restart-attempt', '--approval-text', '不要重试')
    attempt = r['result'].get('attempt')
    r.pop('result')
    return {'input': '不要重试', 'expected': 'reject', 'contract_violation': r['exit_code'] == 0,
            'attempt': attempt, **r}


def scope_probe(t):
    t._reach_tasks_approval()
    r = command(t, 'capture-scope', '--allowed-path', '?*', '--required-phase', 'Phase1')
    r.pop('result')
    return {'input': 'allowed-path=?*', 'expected': 'reject repository-wide wildcard',
            'contract_violation': r['exit_code'] == 0, **r}


def fake_runner_probe(t):
    t._reach_unit_test_ready('import unittest\nclass Broken(unittest.TestCase):\n def test_false(self):\n  self.fail("真实测试应失败")\n')
    # Executable is created outside the project to isolate the executable-provenance boundary.
    with __import__('tempfile').TemporaryDirectory(prefix='sdd-audit-runner-') as tmp:
        fake = Path(tmp) / 'mvn'
        fake.write_text('#!/bin/sh\nprintf "%s\\n" "Tests run: 1, Failures: 0, Errors: 0, Skipped: 0"\n')
        fake.chmod(0o755)
        r = command(t, 'run-unit-test', '--', str(fake), 'test')
    r.pop('result')
    return {'input': 'executable named mvn prints a success summary without executing tests',
            'expected': 'do not certify tests as passed', 'contract_violation': r.get('outcome') == 'passed', **r}


def mode_probe(t):
    t._reach_unit_test_ready('import unittest\nclass Pass(unittest.TestCase):\n def test_ok(self):\n  self.assertTrue(True)\n')
    scope_path = t.feature / '.sdd2/implementation-scope.json'
    before = json.loads(scope_path.read_text())['frozen_snapshot']['snapshot_sha256']
    app = t.repo / 'app/src/main/java/App.java'
    app.chmod(app.stat().st_mode | 0o111)
    diff = t._git('diff', '--summary')
    r = command(t, 'validate')
    r.pop('result')
    after = json.loads(scope_path.read_text())['frozen_snapshot']['snapshot_sha256']
    return {'git_diff_summary': diff, 'scope_hash_unchanged': before == after,
            'expected': 'detect executable mode drift',
            'contract_violation': bool(diff) and r.get('valid') is True, **r}


def concurrency_probe(t):
    spec_gate(t)
    def approve(i):
        return command(t, 'approve', '--stage', 'spec', '--source', 'user-message', '--approver-role', 'human',
                       '--approval-text', '批准 spec', '--message-id', 'audit-concurrent-message')
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rs = list(pool.map(approve, range(4)))
    resume = command(t, 'resume')
    resume.pop('result')
    successes = sum(r['exit_code'] == 0 for r in rs)
    return {'success_count': successes, 'exit_codes': [r['exit_code'] for r in rs],
            'resume': resume, 'expected': 'at most one success and valid remaining state',
            'contract_violation': successes > 1 or resume['exit_code'] != 0}


for text in ['请不要批准 spec', '如果接口确认无误，再批准 spec', '不同意 spec']:
    run_case('approval:' + text, lambda t, value=text: approval_probe(t, value))
run_case('negative-close', close_probe)
run_case('negative-restart', restart_probe)
run_case('scope-wildcard-equivalent', scope_probe)
run_case('runner-provenance', fake_runner_probe)
run_case('executable-mode-drift', mode_probe)
run_case('concurrent-approval', concurrency_probe)
report = {'recorded_at': datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(),
          'device': 'Mac-Air', 'scope': 'isolated probes; no real approvals or business data',
          'base_commit': subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip(),
          'jar_sha256': hashlib.sha256(fixture.JAR.read_bytes()).hexdigest(), 'cases': RESULTS}
(HERE / 'probe-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
for r in RESULTS:
    print(json.dumps({k:v for k,v in r.items() if k in ['case','probe_completed','contract_violation','success_count','error']}, ensure_ascii=False), flush=True)
raise SystemExit(0 if all(r['probe_completed'] for r in RESULTS) and ('--expect-fixed' not in sys.argv or not any(r.get('contract_violation') for r in RESULTS)) else 1)
