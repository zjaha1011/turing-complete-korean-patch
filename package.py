from pathlib import Path
import hashlib,json,zipfile
import validate
root=Path(__file__).resolve().parent
validate.validate(root)
cfg=json.loads((root/'compat.json').read_text(encoding='utf-8'))
manifest=json.loads((root/'payload-manifest.json').read_text(encoding='utf-8'))
actual={p.relative_to(root/cfg['game']).as_posix() for p in (root/cfg['game']).rglob('*') if p.is_file()}
assert actual==set(manifest),'Payload contains missing or unexpected files'
for rel,expected in manifest.items():
 assert hashlib.sha256((root/cfg['game']/rel).read_bytes()).hexdigest()==expected,rel
out=root/'dist';out.mkdir(exist_ok=True)
path=out/(cfg['game'].replace(' ','')+'-Korean.zip')
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted((root/cfg['game']).rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root))
 for name in ['README.md','THIRD_PARTY.md','LICENSE','COMPATIBILITY.md','KoreanPatcher.cmd','patcher.py','validate.py','compat.json','contracts.json','payload-manifest.json']:
  z.write(root/name,name)
print(path)
print(hashlib.sha256(path.read_bytes()).hexdigest())
