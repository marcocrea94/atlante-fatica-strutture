"""Native SVG engineering diagrams. All coordinates below are authored geometry.

No PDF graphics, raster tracing, embedded bitmaps or image processing is used.
Dimensions are symbolic; diagrams deliberately have no physical scale.
"""
from html import escape
import math

INK='#173d59'; BLUE='#8bc6eb'; LIGHT='#d2eafa'; SIDE='#4596c7'
WELD='#ee8b31'; EDGE='#be571d'; FORCE='#007f83'; MARK='#ab3760'

class Drawing:
 def __init__(self):self.items=[]
 def add(self,s):self.items.append(s)
 def group(self,transform):self.add(f'<g transform="{transform}">')
 def end(self):self.add('</g>')
 def path(self,d,fill='none',stroke=INK,width=2.3,extra=''):
  self.add(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')
 def poly(self,points,fill=BLUE,stroke=INK,width=2.3):
  self.path('M'+' L'.join(f'{x:g},{y:g}' for x,y in points)+' Z',LIGHT if fill=='url(#metal)' else fill,stroke,width)
  if fill=='url(#metal)':self.hatch(points)
 def hatch(self,points):
  # Intersect x+y=k hatch lines with polygon edges; entirely native paths.
  for k in range(int(min(x+y for x,y in points)//14)*14,int(max(x+y for x,y in points))+1,14):
   hits=[]
   for a,b in zip(points,points[1:]+points[:1]):
    den=(b[0]+b[1])-(a[0]+a[1])
    if den:
     t=(k-a[0]-a[1])/den
     if 0<=t<1:hits.append((a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])))
   hits.sort()
   for j in range(0,len(hits)-1,2):self.line(hits[j],hits[j+1],'#65a2cb',1)
 def rect(self,x,y,w,h,fill=BLUE,rx=0):
  self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{LIGHT if fill=="url(#metal)" else fill}" stroke="{INK}" stroke-width="2.3"/>')
  if fill=='url(#metal)':self.hatch([(x,y),(x+w,y),(x+w,y+h),(x,y+h)])
 def ellipse(self,x,y,rx,ry,fill=LIGHT,stroke=INK,width=2.3):
  self.add(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
 def text(self,x,y,t,size=21,color=INK,anchor='start'):
  self.add(f'<text x="{x:g}" y="{y:g}" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" text-anchor="{anchor}">{escape(str(t))}</text>')
 def line(self,a,b,color=INK,width=2.3,dash=None):
  self.path(f'M{a[0]:g},{a[1]:g} L{b[0]:g},{b[1]:g}',stroke=color,width=width,extra=f'stroke-dasharray="{dash}"' if dash else '')
 def arrow(self,a,b,label=None):
  self.line(a,b,FORCE,3.2);self.head(a,b,FORCE,14)
  if label:self.text((a[0]+b[0])/2,(a[1]+b[1])/2-14,label,21,FORCE,'middle')
 def head(self,a,b,color=INK,size=8):
  length=math.dist(a,b)
  if not length:return
  dx=(b[0]-a[0])/length;dy=(b[1]-a[1])/length
  self.poly([b,(b[0]-size*dx+size*.32*dy,b[1]-size*dy-size*.32*dx),(b[0]-size*dx-size*.32*dy,b[1]-size*dy+size*.32*dx)],color,color,1)
 def dim(self,a,b,label,offset=0):
  a1=(a[0],a[1]+offset);b1=(b[0],b[1]+offset)
  if offset:self.line(a,a1,INK,1);self.line(b,b1,INK,1)
  self.line(a1,b1,INK,1.2);self.head(b1,a1);self.head(a1,b1)
  vertical=abs(a1[0]-b1[0])<15
  self.text((a1[0]+b1[0])/2+(18 if vertical else 0),(a1[1]+b1[1])/2+(-9 if not vertical else 6),label,20,INK,'middle')
 def leader(self,a,b,label,color=INK):
  self.line(a,b,color,1.5);self.ellipse(*a,3,3,color,color);self.text(b[0]+7,b[1]-5,label,20,color)
 def weld(self,a,b,width=10,flush=False):
  self.line(a,b,WELD,width)
  length=math.dist(a,b);n=max(1,int(length/12));dx=(b[0]-a[0])/length;dy=(b[1]-a[1])/length
  if not flush:
   for i in range(n):
    x=a[0]+(i+.5)*(b[0]-a[0])/n;y=a[1]+(i+.5)*(b[1]-a[1])/n
    self.path(f'M{x-dy*width/2:g},{y+dx*width/2:g} q{dx*5:g},{dy*5:g} {dy*width:g},{-dx*width:g}',stroke=EDGE,width=1)
 def iso(self,x,y,z=0):return (110+x+.55*y,325-.35*y-z)
 def face(self,pts,fill=BLUE):self.poly([self.iso(*p) for p in pts],fill)
 def plate(self,x=35,y=0,z=0,L=440,B=135,T=12):
  self.face([(x,y,z),(x+L,y,z),(x+L,y,z+T),(x,y,z+T)],SIDE)
  self.face([(x+L,y,z),(x+L,y+B,z),(x+L,y+B,z+T),(x+L,y,z+T)],BLUE)
  self.face([(x,y,z+T),(x+L,y,z+T),(x+L,y+B,z+T),(x,y+B,z+T)],LIGHT)
 def seam(self,x,y,z,X,Y,Z,flush=False):self.weld(self.iso(x,y,z),self.iso(X,Y,Z),flush=flush)
 def axial(self,z=30,y=25):
  self.arrow(self.iso(95,y,z),self.iso(20,y,z));self.arrow(self.iso(450,y,z),self.iso(525,y,z),'Δσ')
 def beam(self,weld=None,butt=None,holes=False,cover=False,box=False,tee=False,show_axial=True):
  self.plate()
  # Web, then top flange; order follows visible surfaces.
  self.plate(35,60,12,440,8,125)
  if box:self.plate(35,127,12,440,8,125)
  if not tee:self.plate(35,0,137,440,135,12)
  if weld:
   self.seam(45,54,14,460,54,14,flush=weld=='flush')
   if weld=='both' and not tee:self.seam(45,54,136,460,54,136)
  if butt:
   self.seam(260,0,149 if not tee else 12,260,135,149 if not tee else 12,flush=butt=='flush')
   self.seam(260,0,12,260,135,12,flush=butt=='flush')
   if butt!='flanges':self.seam(260,58,17,260,58,133,flush=butt=='flush')
  if cover:
   self.plate(235,5,149,200,125,10);self.plate(235,5,12,200,125,10)
  if holes or cover:
   for z in [160 if cover else 149,23 if cover else 12]:
    for x in [270,330,400]:
     for y in [22,108]:
      p=self.iso(x,y,z);self.ellipse(*p,5,2.5,'#486578' if cover else 'white')
  if show_axial:self.axial(175)
 def bolt(self,x,y,z):
  px,py=self.iso(x,y,z);self.ellipse(px,py,7,4,'#496a82');self.ellipse(px,py-5,7,4,'#b3c9d8');self.line((px-7,py),(px-7,py-5))
 def plate_joint(self,mode='butt',flush=False,cap=None):
  self.plate()
  if mode in ['butt','one_sided','partial']:
   self.seam(250,0,13,250,135,13,flush)
   if mode=='one_sided':self.leader(self.iso(250,0,8),(380,373),'radice',MARK)
  elif mode=='long':self.seam(45,68,13,465,68,13,flush)
  elif mode=='cover':
   self.plate(180,5,12,230,125,12);self.plate(180,5,-12,230,125,12)
   for x in [210,280,370]:
    for y in [27,103]:self.bolt(x,y,26)
  elif mode=='lap':
   self.plate(210,0,12,290,135,12);self.seam(210,0,26,210,135,26)
   self.seam(350,0,12,350,135,12)
  self.axial(40)
  if cap:self.text(400,150,cap,22,EDGE,'middle')
 def butt_section(self,style='x',flush=False,backing=False,partial=False,offset=False,step=False):
  y=230;h=45
  self.rect(145,y,255,h,'url(#metal)');self.rect(400,y+(13 if offset else 0),255,h,'url(#metal)')
  top=y-(0 if flush else 12);bot=y+h+(0 if flush else 12)
  if style=='v':p=f'M370,{top} Q400,{top-8 if not flush else top} 430,{top} L407,{y+h} L393,{y+h} Z'
  else:p=f'M370,{top} Q400,{top-6 if not flush else top} 430,{top} L406,{y+h/2} L430,{bot} Q400,{bot+6 if not flush else bot} 370,{bot} L394,{y+h/2} Z'
  self.path(p,WELD,EDGE,2)
  if partial:self.rect(393,y+17,14,13,'white');self.leader((400,y+24),(473,345),'radice',MARK)
  if backing:self.rect(347,y+h,106,19,'url(#metal)');self.text(400,340,'sostegno al rovescio',20,INK,'middle')
  if step:self.rect(145,y-20,240,20,'url(#metal)');self.rect(145,y+h,240,20,'url(#metal)')
  self.arrow((137,252),(75,252),'Δσ');self.arrow((663,252),(725,252))
  self.dim((675,y),(675,y+h),'t')
 def tube(self,rect=False,seam=None,collar=False,show_axial=True):
  if rect:
   self.plate(50,0,0,415,130,100)
   self.face([(465,8,8),(465,122,8),(465,122,92),(465,8,92)],'white')
  else:
   self.path('M180,211 L585,171 A48,69 0 0 1 605,309 L200,349 A48,69 0 0 0 180,211',LIGHT)
   self.ellipse(595,240,49,70,BLUE);self.ellipse(595,240,38,57,'white')
   self.line((180,211),(585,171));self.line((200,349),(605,309))
  if seam=='long':
   if rect:self.seam(65,65,101,450,65,101)
   else:self.weld((220,255),(560,221))
  if seam=='butt' or collar:
   if rect:
    self.seam(260,0,100,260,130,100);self.seam(260,0,0,260,0,100)
   else:self.path('M388,191 A48,69 0 0 1 408,329',stroke=WELD,width=12)
  if collar:
   if rect:self.plate(257,-18,-16,14,166,133)
   else:
    self.path('M390,157 A67,91 0 0 1 412,359 L422,358 A67,91 0 0 0 400,156 Z',BLUE)
    self.path('M390,175 A55,75 0 0 1 410,342',stroke=WELD,width=9)
  if show_axial:self.arrow((165,275),(88,282),'Δσ');self.arrow((660,232),(729,225))
 def attachment(self,kind='long',rounded=False,taper=False,side=False):
  self.plate()
  if kind=='stud':
   p=self.iso(280,70,12);self.rect(p[0]-10,p[1]-130,20,122,BLUE);self.ellipse(p[0],p[1]-131,17,6,LIGHT);self.ellipse(p[0],p[1]-6,18,7,WELD)
  elif kind=='transverse':
   self.plate(285,10,12,8,115,98);self.seam(281,10,14,281,125,14)
   self.dim(self.iso(285,10,125),self.iso(293,10,125),'ℓ')
  elif kind=='flat':
   self.plate(205,-62,0,140,62,12);self.seam(205,0,13,345,0,13)
  elif kind=='patch':
   self.plate(210,25,12,160,85,12)
   for a,b in [((210,25,24),(370,25,24)),((370,25,24),(370,110,24)),((210,110,24),(370,110,24)),((210,25,24),(210,110,24))]:self.seam(*a,*b)
  else:
   x=190;y=-2 if side else 63;end=390;z=13
   pts=[self.iso(x,y,z),self.iso(end,y,z)]
   if rounded:
    a=self.iso(x,y,z);b=self.iso(end,y,z);c=self.iso(end-65,y,z+115);e=self.iso(x+65,y,z+115)
    self.path(f'M{a[0]},{a[1]} L{b[0]},{b[1]} Q{c[0]},{a[1]} {c[0]},{c[1]} L{e[0]},{e[1]} Q{e[0]},{a[1]} {a[0]},{a[1]} Z',BLUE)
   else:
    pts += [self.iso(end-(40 if taper else 0),y,z+105),self.iso(x+(40 if taper else 0),y,z+105)];self.poly(pts,BLUE)
   self.seam(x,y-5,z+2,end,y-5,z+2)
   self.dim(self.iso(x,y,145),self.iso(end,y,145),'L')
   if rounded:self.leader(self.iso(x+28,y,60),(230,188),'r')
   elif taper:self.text(355,225,'α',24)
  self.axial(45,15)
 def cross_section(self,partial=False,single=False,nonload=False,misalignment=False,ground=False):
  self.rect(175,243,450,30,'url(#metal)')
  self.rect(385,145,30,220 if not nonload else 98,'url(#metal)')
  for x,sgn in [(385,-1),(415,1)]:
   self.poly([(x,243),(x+sgn*28,243),(x,215)],WELD,EDGE)
   if not single and not nonload:self.poly([(x,273),(x+sgn*28,273),(x,301)],WELD,EDGE)
  if partial:self.line((385,247),(385,269),MARK,4);self.line((415,247),(415,269),MARK,4)
  elif not nonload:
   for x,s in [(385,-1),(415,1)]:
    if single:self.poly([(x,216),(x+s*30,243),(x,273)],WELD,EDGE)
    else:self.poly([(x,219),(x+s*27,243),(x+s*6,258),(x+s*27,273),(x,297)],WELD,EDGE)
  if ground:self.text(400,125,'raccordo molato',20,EDGE,'middle')
  self.arrow((160,258),(90,258),'Δσ');self.arrow((640,258),(710,258))
  self.dim((650,243),(650,273),'t')
  if partial:self.leader((415,257),(497,340),'radice',MARK)
 def lap_section(self,double=False):
  if not double:
   self.rect(150,268,320,35,'url(#metal)');self.rect(330,233,320,35,'url(#metal)')
   self.poly([(310,268),(330,248),(330,268)],WELD,EDGE);self.poly([(470,268),(490,268),(470,288)],WELD,EDGE)
   self.arrow((144,286),(78,286),'Δσ');self.arrow((655,251),(723,251))
   return
  self.rect(150,252,270,33,'url(#metal)');self.rect(420,252,225,33,'url(#metal)')
  self.rect(270,219,255,33,'url(#metal)')
  for x,sgn in [(270,-1),(525,1)]:self.poly([(x,219),(x+sgn*28,252),(x,252)],WELD,EDGE)
  if double:
   self.rect(270,285,255,33,'url(#metal)')
   for x,sgn in [(270,-1),(525,1)]:self.poly([(x,318),(x+sgn*28,285),(x,285)],WELD,EDGE)
  self.arrow((145,269),(78,269),'Δσ');self.arrow((650,269),(723,269))
 def tube_section(self,shape='round',intermediate=False,fillet=False,backing=False):
  self.rect(150,196,430,110,LIGHT,5 if shape=='rect' else 0)
  self.line((150,213),(580,213),INK,1.3,'8 6');self.line((150,289),(580,289),INK,1.3,'8 6')
  if intermediate:
   self.rect(354,179,20,144,BLUE)
   for x,sgn in [(354,-1),(374,1)]:
    self.poly([(x,196),(x+sgn*18,196),(x,179)],WELD,EDGE)
    self.poly([(x,306),(x+sgn*18,306),(x,323)],WELD,EDGE)
  else:self.rect(355,196,14,110,WELD)
  if shape=='round':self.ellipse(675,251,49,49,LIGHT);self.ellipse(675,251,37,37,'white')
  else:self.rect(627,203,96,96,LIGHT,11);self.rect(639,215,72,72,'white',7)
  self.arrow((260,251),(180,251),'Δσ');self.arrow((450,251),(540,251))
  if backing:self.rect(325,217,72,13,BLUE);self.rect(325,276,72,13,BLUE)
  if intermediate:self.text(365,362,'cordoni d’angolo' if fillet else 'piena penetrazione',21,EDGE,'middle')
 def flange_section(self,mode='fillet',through=False,solid=False,backing=False):
  self.rect(180,290,440,38,'url(#metal)')
  self.rect(305,165,24,125+(72 if through else 0),'url(#metal)');self.rect(471,165,24,125+(72 if through else 0),'url(#metal)')
  if not solid:self.rect(329,290,142,38,'white')
  for x,sgn in [(305,-1),(495,1)]:
   self.poly([(x,290),(x+sgn*28,290),(x,262)],WELD,EDGE)
   if mode=='full' or through:self.poly([(x,328),(x+sgn*25,328),(x,353)],WELD,EDGE)
  if backing:self.rect(331,266,25,24,BLUE);self.rect(444,266,25,24,BLUE)
  self.line((400,140),(400,380),INK,1,'14 5 3 5');self.arrow((400,153),(400,220),'Δσ')
  self.arrow((178,310),(105,310));self.arrow((623,310),(696,310))
 def runway(self,variant=1,load=True):
  if variant in [1,5,6,7]:
   root=285 if variant==5 else 320 if variant in [6,7] else 358
   self.path(f'M180,191 L620,191 L620,222 L450,222 Q418,222 418,253 L418,{root} L382,{root} L382,253 Q382,222 350,222 L180,222 Z',LIGHT)
   if variant>=5:
    self.rect(390,root,20,365-root,BLUE);self.weld((388,root),(412,root),8,variant==5)
  else:
   self.rect(180,191,440,31,LIGHT);self.rect(390,222,20,136,BLUE)
   self.poly([(365,222),(390,222),(390,247)],WELD,EDGE)
   self.poly([(410,222),(435,222),(410,247)],WELD,EDGE)
   if variant in [2,3]:
    self.poly([(375,222),(400,204),(425,222),(400,247)],WELD,EDGE)
    if variant==3:self.line((397,222),(403,222),MARK,5)
  if load:self.arrow((400,112),(400,177),'F')
 def finish(self,title,subtitle,description,compact=False):
  defs='''<defs><marker id="force" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#007f83"/></marker><marker id="dim" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 Z" fill="#173d59"/></marker><pattern id="metal" width="13" height="13" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="13" height="13" fill="#d2eafa"/><path d="M0,0 V13" stroke="#65a2cb" stroke-width="1"/></pattern></defs>'''
  art=''.join(self.items)
  if compact:return f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="430" viewBox="55 100 690 300" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>{defs}<rect x="55" y="100" width="690" height="300" fill="white"/>'+art+'</svg>\n'
  self.items=[]
  self.text(32,43,title,26);self.text(32,74,subtitle,17,'#55738a')
  self.line((32,92),(768,92),'#dbe8f0',1)
  self.line((32,410),(768,410),'#dbe8f0',1)
  for x,c,label in [(38,BLUE,'Metallo'),(213,WELD,'Saldatura'),(416,FORCE,'Azione')]:
   self.ellipse(x,444,5,5,c,c);self.text(x+14,451,label,17,'#426177')
  self.text(767,483,'SCHEMA NON IN SCALA',14,'#718b9e','end')
  return f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" viewBox="0 0 800 500" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>{defs}<rect width="800" height="500" fill="white"/>'+art+''.join(self.items)+'</svg>\n'
