"""Make a reviewable ZIP containing only files changed from a GitHub tree snapshot.

Usage: python scripts/package_update.py BASE_TREE_JSON OUTPUT_ZIP
The snapshot is the public GitHub Git Trees API response, saved by the publisher.
This command never performs a network or repository mutation.
"""
from pathlib import Path
import sys,json,hashlib,zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
 tree=json.loads(Path(sys.argv[1]).read_text(encoding='utf8'));target=Path(sys.argv[2]).resolve()
 base={p['path']:p['sha'] for p in tree['tree'] if p['type']=='blob'}
 assert not tree.get('truncated'),'A complete baseline tree is required'
 valid={r['id'] for r in json.loads((ROOT/'data/details.json').read_text(encoding='utf8'))}
 allowed={'assets','data','docs','scripts','sources','web','README.md','llms.txt','llms-full.txt','requirements.txt','requirements-build.txt','.gitignore'}
 entries=[]
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(ROOT.rglob('*')):
   if not p.is_file():continue
   rel=p.relative_to(ROOT)
   if rel.parts[0] not in allowed or '__pycache__' in rel.parts:continue
   if rel.parts[:2]==('docs','details') and p.stem not in valid:continue
   data=p.read_bytes();digest=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
   if base.get(rel.as_posix())==digest:continue
   z.writestr(rel.as_posix(),data);entries.append({'path':rel.as_posix(),'git_blob_sha':digest})
 report={'baseline':tree['sha'],'archive':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'files':entries}
 target.with_suffix('.manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps({**report,'files':len(entries)},ensure_ascii=False))
if __name__=='__main__':main()
