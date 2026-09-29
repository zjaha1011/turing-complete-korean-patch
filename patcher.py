"""Optional offline installer. Python 3.10+, standard library only."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,shutil,subprocess,sys,tempfile,uuid

def digest(data):return hashlib.sha256(data).hexdigest()
def read_json(path):return json.loads(path.read_text(encoding='utf-8'))
def safe(root,rel):
 p=(root/rel).resolve()
 if not p.is_relative_to(root.resolve()) or p==root.resolve():raise ValueError('Unsafe relative path: '+str(rel))
 return p
def atomic(path,data):
 path.parent.mkdir(parents=True,exist_ok=True)
 fd,name=tempfile.mkstemp(prefix='.korean-',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(name,path)
 finally:
  if os.path.exists(name):os.unlink(name)
def discover(game):
 roots=[]
 if os.name=='nt':
  import winreg
  for hive,key,value in [(winreg.HKEY_CURRENT_USER,r'Software\Valve\Steam','SteamPath'),(winreg.HKEY_LOCAL_MACHINE,r'SOFTWARE\WOW6432Node\Valve\Steam','InstallPath')]:
   try:
    with winreg.OpenKey(hive,key) as k:roots.append(Path(winreg.QueryValueEx(k,value)[0]))
   except OSError:pass
 roots.append(Path(os.environ.get('ProgramFiles(x86)',r'C:\Program Files (x86)'))/'Steam')
 libraries=list(roots)
 for root in roots:
  vdf=root/'steamapps/libraryfolders.vdf'
  if vdf.is_file():
   for item in re.findall(r'"(?:path|\d+)"\s+"([^"\r\n]+)"',vdf.read_text(encoding='utf-8')):
    if re.match(r'^[A-Za-z]:[\\/]',item):libraries.append(Path(item.replace('\\\\','\\')))
 return sorted({p.resolve() for root in libraries if (p:=root/'steamapps/common'/game).is_dir()})
def ensure_closed(exe):
 if os.name!='nt':return
 result=subprocess.run(['tasklist','/FO','CSV','/NH'],capture_output=True,text=True,errors='replace',check=True)
 if any(line.lower().startswith('"'+exe.lower()+'",') for line in result.stdout.splitlines()):raise RuntimeError('게임을 완전히 종료한 뒤 다시 실행하세요: '+exe)
def menu_patch(data,config):
 before=config['before'].encode('utf-8');after=config['after'].encode('utf-8')
 if len(before)!=len(after):raise ValueError('Menu signature byte lengths differ')
 a,b=data.count(before),data.count(after)
 if a==0 and b==1 and digest(data) in config['patched_sha256']:return data,'already applied'
 if a!=1 or b!=0:return None,f'skipped: signature counts before={a}, after={b}'
 if digest(data) not in config['original_sha256']:return None,'skipped: unknown executable version'
 result=data.replace(before,after,1)
 if digest(result) not in config['patched_sha256']:return None,'skipped: output hash mismatch'
 return result,'applied'

class Installer:
 def __init__(self,root):
  self.root=root.resolve();self.state=self.root/'_korean_patch_state/v2'
  self.state.mkdir(parents=True,exist_ok=True)
  self.manifest=self.state/'manifest.json'
  self.entries=read_json(self.manifest) if self.manifest.exists() else {}
  self.reports=[]
  self.backup=self.root/'_korean_patch_backup'/('v2-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8])
 def save(self):atomic(self.manifest,json.dumps(self.entries,ensure_ascii=False,indent=2).encode('utf-8'))
 def write(self,rel,data,repair=False):
  target=safe(self.root,rel);current=target.read_bytes() if target.exists() else None
  expected=digest(data)
  if current==data:
   # A manual copy has no trustworthy pre-patch backup. Never call that an original.
   self.reports.append([rel,'already present']);return
  entry=self.entries.get(rel)
  if entry and current is not None and digest(current) not in [entry['installed'],entry.get('original')]:
   if not repair:raise RuntimeError('다른 변경 또는 게임 업데이트를 감지했습니다. 기본 번역을 다시 설치하려면 --repair를 사용하세요: '+rel)
   archive=self.state/('history-'+uuid.uuid4().hex+'.json')
   atomic(archive,json.dumps({rel:entry},ensure_ascii=False,indent=2).encode('utf-8'))
   self.backup=self.root/'_korean_patch_backup'/('v2-repair-'+uuid.uuid4().hex)
   entry=None
  if not entry:
   backup=None
   if current is not None:
    bp=safe(self.backup,rel);bp.parent.mkdir(parents=True,exist_ok=True)
    with bp.open('xb') as f:f.write(current)
    backup=str(bp.relative_to(self.root))
   entry={'backup':backup,'original':digest(current) if current is not None else None,'installed':expected}
   self.entries[rel]=entry
  else:entry['installed']=expected
  # Record recovery information before replacing the destination.
  self.save();atomic(target,data)
  if digest(target.read_bytes())!=expected:raise IOError('Readback mismatch: '+rel)
  self.reports.append([rel,'applied'])
 def uninstall(self):
  for rel,entry in list(self.entries.items()):
   target=safe(self.root,rel)
   current=digest(target.read_bytes()) if target.is_file() else None
   if current==entry.get('original'):
    self.reports.append([rel,'already restored']);del self.entries[rel];self.save();continue
   if current!=entry['installed']:
    self.reports.append([rel,'skipped: changed after installation']);continue
   if entry['backup']:
    original=safe(self.root,entry['backup']).read_bytes()
    if digest(original)!=entry['original']:raise IOError('Backup hash mismatch: '+rel)
    atomic(target,original)
   else:target.unlink()
   del self.entries[rel];self.save();self.reports.append([rel,'restored'])
 def report(self):
  print(json.dumps(self.reports,ensure_ascii=False,indent=2))
  atomic(self.state/'last-result.json',json.dumps(self.reports,ensure_ascii=False,indent=2).encode('utf-8'))

class InstallLock:
 def __init__(self,root):self.path=root/'_korean_patch_state/installer.lock'
 def __enter__(self):
  self.path.parent.mkdir(parents=True,exist_ok=True)
  try:
   with self.path.open('x',encoding='utf-8') as f:f.write(str(os.getpid()))
  except FileExistsError:raise RuntimeError('다른 설치가 진행 중이거나 이전 설치가 중단되었습니다. 패처가 모두 종료되었는지 확인 후 _korean_patch_state/installer.lock을 제거하세요.')
 def __exit__(self,*args):self.path.unlink()

def main():
 here=Path(__file__).resolve().parent;cfg=read_json(here/'compat.json')
 parser=argparse.ArgumentParser(description=cfg['game']+' 한국어 패치')
 parser.add_argument('--game-path',type=Path)
 mode=parser.add_mutually_exclusive_group();mode.add_argument('--uninstall',action='store_true');mode.add_argument('--repair',action='store_true');mode.add_argument('--menu-only',action='store_true')
 args=parser.parse_args()
 candidates=discover(cfg['game']) if args.game_path is None else [args.game_path]
 if len(candidates)!=1:raise RuntimeError('게임 폴더를 지정하세요: --game-path "전체 경로"; 발견된 경로: '+str(candidates))
 root=candidates[0].resolve()
 if not (root/cfg['exe']).is_file():raise RuntimeError('게임 실행 파일이 없습니다: '+str(root))
 ensure_closed(cfg['exe'])
 with InstallLock(root):apply(here,cfg,root,args)

def apply(here,cfg,root,args):
 installer=Installer(root)
 try:
  if args.uninstall:installer.uninstall();return
  if not args.menu_only:
   payload=here/cfg['game']
   if payload.resolve()==root:raise RuntimeError('게임 폴더 밖에 압축을 푼 새 ZIP에서 패처를 실행하세요.')
   import validate
   validate.validate(here)
   manifest=read_json(here/'payload-manifest.json')
   # Validate every source before writing anything.
   for rel,sha in manifest.items():
    if digest(safe(payload,rel).read_bytes())!=sha:raise RuntimeError('패치 파일이 손상되었습니다: '+rel)
   version_file=cfg.get('version_file')
   version=(root/version_file).read_text(encoding='utf-8').splitlines()[0] if version_file else digest((root/cfg['exe']).read_bytes())
   supported=any(x in version for x in cfg['known_versions'])
   for rel,expected in cfg.get('original_game_hashes',{}).items():
    if not safe(root,rel).is_file() or digest(safe(root,rel).read_bytes())!=expected:
     supported=False;installer.reports.append([rel,'original differs; verify game files before optional plug-in use'])
   installer.reports.append(['version','known' if supported else 'unknown; optional enhancements skipped'])
   for rel in manifest:
    # Repair only the basic translations/fonts. Preserve optional plug-in files.
    if rel.startswith('BepInEx/') and (args.repair or not supported):
     installer.reports.append([rel,'skipped']);continue
    installer.write(rel,safe(payload,rel).read_bytes(),repair=args.repair)
  if cfg.get('menu') and not args.repair:
   target=root/cfg['exe'];data,status=menu_patch(target.read_bytes(),cfg['menu'])
   if data is not None:installer.write(cfg['exe'],data)
   installer.reports.append(['menu',status])
 except Exception as e:
  installer.reports.append(['failure',str(e)]);raise
 finally:installer.report()

if __name__=='__main__':
 try:main()
 except Exception as e:print('오류:',e,file=sys.stderr);sys.exit(1)
