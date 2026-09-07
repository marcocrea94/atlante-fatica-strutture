"""Package the reviewed source tree, excluding generated site/cache files."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
target=ROOT.parent/'atlante-fatica-source.zip'
valid={r['id'] for r in json.loads((ROOT/'data/details.json').read_text(encoding='utf8'))}
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(ROOT)
  if any(v in ['site','.git','__pycache__','.venv'] for v in rel.parts):continue
  if rel.parts[:2]==('docs','details') and p.stem not in valid:continue
  z.write(p,rel.as_posix())
print(json.dumps({'path':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))
