"""Recover text from raster pages / broken font encodings. Never infer formulas."""
from pathlib import Path
import json, sys, numpy as np
import pymupdf
from rapidocr import RapidOCR
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
engine=RapidOCR(params={'EngineConfig.onnxruntime.intra_op_num_threads':4,'EngineConfig.onnxruntime.inter_op_num_threads':2,'Global.max_side_len':2600,'Global.log_level':'warning'})
for src,numbers in [('ntc',list(range(123,135))+[171,172,176]),('iiw',[46])]:
 d=pymupdf.open(ROOT/'sources'/f'{src}.pdf')
 for num in numbers:
  target=ROOT/'data'/'ocr'/f'{src}-{num:03}.json'
  if target.exists(): continue
  p=d[num-1]; pix=p.get_pixmap(dpi=220)
  img=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,3)
  result=engine(img)
  records=[]
  if result.txts:
   for box,txt,score in zip(result.boxes,result.txts,result.scores):
    b=np.asarray(box)*72/220
    records.append({'bbox':[float(b[:,0].min()),float(b[:,1].min()),float(b[:,0].max()),float(b[:,1].max())],'text':txt,'confidence':float(score)})
  target.parent.mkdir(parents=True,exist_ok=True)
  target.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
  print(src,num,len(records),flush=True)
