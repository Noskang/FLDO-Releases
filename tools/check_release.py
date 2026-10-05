from pathlib import Path
import json,re,subprocess
r=Path(__file__).resolve().parents[1]
d=json.loads((r/'current-release.json').read_text())
assert d['schemaVersion']==1 and d['gameRebuilt'] is False
assert re.fullmatch(r'[a-f0-9]{64}',d['sha256'])
assert 0<d['bytes']<2*1024**3
assert d['artifact'].endswith('.zip') and '/' not in d['artifact']
paths=subprocess.check_output(['git','-C',str(r),'ls-files','-z']).decode().split('\0')
allowed={'README.md','current-release.json','.gitignore','.gitattributes','tools/check_release.py','.github/workflows/release-metadata.yml','.github/pull_request_template.md'}
assert all(not p or p in allowed for p in paths),'Unreviewed public file'
for p in paths:
 if not p:continue
 b=(r/p).read_text()
 assert not re.search(r'[A-Za-z]:[\\/](?:Users|Work)[\\/]',b),'Absolute local path'
print('Public release metadata and tracked allowlist: PASS')
