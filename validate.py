from pathlib import Path
import json,re,collections,xml.etree.ElementTree as ET,hashlib,sys
def xml_records(p):
 root=ET.parse(p).getroot(); out={}; counts=collections.Counter()
 for section in root:
  if not len(section):continue
  for record in section:
   if record.tag=='String':
    k=f'{section.tag}/String/{counts[section.tag]}';counts[section.tag]+=1;out[k]=record.text or '';continue
   key=record.findtext('Key')
   identity=f'{section.tag}/{key}';n=counts[identity];counts[identity]+=1
   for field in record:
    if field.tag=='Key':continue
    out[f'{identity}/{n}/{field.tag}']=field.text or ''
 return out
def tc_records(p,english=False):
 s=p.read_bytes().decode('utf-8').replace('\r\n','\n'); out={}
 boundaries=list(re.finditer(r'^\$(\d+)\*[ \n]?|^=== .* ===\n',s,re.M))
 for i,m in enumerate(boundaries):
  if not m[1]:continue
  value=s[m.end():boundaries[i+1].start() if i+1<len(boundaries) else len(s)]
  # Remove record delimiters only; preserve leading whitespace and trailing spaces.
  value=value.rstrip('\n')
  if english:
   assert value.startswith(m[1]+' '),(p,m[1]);value=value[len(m[1])+1:]
  assert m[1] not in out,('duplicate ID',m[1]);out[m[1]]=value
 return out
def tokens(s,game):
 if game=='station':
  s=re.sub(r'\{((?:LINK|THING):[^;}]+);[^}]+\}',r'{\1}',s)
  s=re.sub(r'\{(HEADER|COLORRED):[^}]+\}',r'{\1}',s)
  s=re.sub(r'\{(THING):\s+',r'{\1:',s)
 pattern=r'\{[^{}\n]+\}|#VAR\d+#|%[a-zA-Z_][a-zA-Z_0-9]*'
 if game=='station':pattern+=r'|</?[A-Za-z][^>]*>'
 else:pattern+=r'|(?<!\\)\[(?:/?(?:b|i|u|s|center|left|right|box|tip|color|image|link|highlight|large|nbsp|T|F|Z|E))(?:=[^\]\n]*)?\]|[\ue85d\uf2db]'
 return dict(sorted(collections.Counter(re.findall(pattern,s)).items()))
def validate(base):
 base=Path(base);cfg=json.loads((base/'compat.json').read_text(encoding='utf-8'))
 contract=json.loads((base/'contracts.json').read_text(encoding='utf-8'))
 results=[];failures=[]
 for rel,expected in contract['files'].items():
  path=base/cfg['game']/rel
  try:
   raw=path.read_bytes();text=raw.decode('utf-8')
   assert not raw.startswith(b'\xef\xbb\xbf'),'UTF-8 BOM'
   if cfg['kind']=='station':
    assert b'\n' not in raw.replace(b'\r\n',b''),'Line endings must be CRLF'
    actual=xml_records(path)
   else:
    assert b'\r' not in raw,'Line endings must be LF'
    actual=tc_records(path)
   assert set(actual)==set(expected),f'Key difference missing={sorted(set(expected)-set(actual))} extra={sorted(set(actual)-set(expected))}'
   for key,value in actual.items():
    reference=expected[key]
    assert tokens(value,cfg['kind'])==reference['tokens'],key+': placeholder/tag mismatch'
    assert not re.search(r'[\ufffd\x00-\x08\x0b\x0c\x0e-\x1f·ㆍ「」“”\uff01-\uff60\U0001f300-\U0001faff]',value),key+': forbidden character'
    assert not reference['nonempty'] or value.strip(),key+': empty translation'
    assert value.count('{')-value.count('}')==reference['brace_delta'],key+': brace structure differs from source'
   results.append({'path':rel,'fields':len(actual)})
  except (AssertionError,ValueError,OSError,ET.ParseError) as e:failures.append(f'{rel}: {e}')
 if cfg['kind']=='turing':
  folder=base/cfg['game']/'translations'
  if (folder/'Korean.txt').read_bytes()!=(folder/'Swedish.txt').read_bytes():failures.append('Korean.txt != Swedish.txt')
 for rel,expected in cfg.get('required_hashes',{}).items():
  path=base/cfg['game']/rel
  if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:failures.append('Required binary/font hash mismatch: '+rel)
 for path in (base/cfg['game']).rglob('*'):
  if not path.is_file():continue
  relative=path.relative_to(base/cfg['game']).as_posix()
  forbidden=path.suffix.lower() in ('.exe','.assets','.ress') or path.name.startswith('level') or path.name=='english.xml' or '/Data/' in relative
  forbidden=forbidden or (path.suffix.lower()=='.dll' and relative!='BepInEx/plugins/StationeersKorean/StationeersKorean.dll')
  if forbidden:failures.append('Game original binary/data is forbidden: '+relative)
 build=base/'plugin-build.json'
 if build.exists():
  for rel,expected in json.loads(build.read_text(encoding='utf-8'))['sha256'].items():
   if hashlib.sha256((base/rel).read_bytes()).hexdigest()!=expected:failures.append('Plugin build/source changed: '+rel)
 if failures:raise ValueError('\n'.join(failures))
 print(json.dumps({'validation':'PASS','files':results,'source_corrections':len(contract['exceptions'])},ensure_ascii=False))
 return results

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--english-dir',type=Path);args=parser.parse_args()
 base=Path(__file__).resolve().parent;validate(base)
 if args.english_dir:
  cfg=json.loads((base/'compat.json').read_text(encoding='utf-8'))
  contract=json.loads((base/'contracts.json').read_text(encoding='utf-8'))
  diff={}
  for rel,known in contract['source_keys'].items():
   name=Path(rel).name.replace('korean','english') if cfg['kind']=='station' else '_ids_and_english.txt'
   fresh=xml_records(args.english_dir/name) if cfg['kind']=='station' else tc_records(args.english_dir/name,True)
   if set(fresh)!=set(known):diff[name]={'new_keys':sorted(set(fresh)-set(known)),'removed_keys':sorted(set(known)-set(fresh))}
  print(json.dumps({'source_key_changes':diff},ensure_ascii=False,indent=2))
  if diff:sys.exit(2)
