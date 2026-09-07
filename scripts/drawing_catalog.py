"""Geometry families used by the explicit, reviewed per-record drawing manifest."""
from drawing_primitives import *

def transition(d,variant):
 d.poly([(150,240),(350,240),(535,180),(650,180),(650,310),(535,310),(350,275),(150,275)],LIGHT)
 d.weld((350,240),(350,275),9,variant=='flush')
 d.arrow((145,257),(80,257),'Δσ');d.arrow((657,248),(723,248))
 d.dim((355,221),(535,161),'raccordo')
 if variant=='backed':d.rect(315,276,85,14,BLUE);d.text(400,358,'Sostegno permanente al rovescio',20,INK,'middle')
 else:d.text(400,358,'Variazione di larghezza / spessore',20,INK,'middle')

def hollow_attachment(d):
 # Elevation and end section of a hollow branch welded below a main member.
 d.rect(155,150,430,88,LIGHT)
 d.line((155,165),(585,165),INK,1.2,'8 5');d.line((155,223),(585,223),INK,1.2,'8 5')
 d.rect(319,239,95,130,BLUE);d.line((334,239),(334,369),INK,1.2,'8 5');d.line((399,239),(399,369),INK,1.2,'8 5')
 d.poly([(304,238),(319,238),(319,255)],WELD,EDGE);d.poly([(414,238),(429,238),(414,255)],WELD,EDGE)
 d.dim((319,391),(414,391),'ℓ');d.rect(635,156,91,84,LIGHT,9);d.rect(647,168,67,60,'white',5)
 d.arrow((288,195),(199,195),'Δσ');d.arrow((458,195),(548,195))

def bolted_flange(d):
 # Perspective view of the tube and its bolted base; two weld-root insets.
 d.ellipse(294,326,149,40,BLUE);d.ellipse(294,315,149,40,LIGHT)
 d.path('M213,174 V304 a81,27 0 0 0 162,0 V174 Z',BLUE)
 d.ellipse(294,174,81,27,LIGHT);d.ellipse(294,174,66,19,'white')
 d.path('M211,304 a83,29 0 0 0 166,0',stroke=WELD,width=10)
 for a in [10,45,90,135,170]:
  x=294+126*math.cos(math.radians(a));y=315+30*math.sin(math.radians(a))
  d.ellipse(x,y,9,4,'#d0dee7');d.rect(x-6,y-8,12,7,'#b4c9d9');d.ellipse(x,y-8,7,3,LIGHT)
 d.arrow((294,135),(294,108));d.text(323,135,'Δσ',21,FORCE)
 for y,label,full in [(169,'11',True),(296,'12',False)]:
  d.rect(542,y-25,22,76,'url(#metal)');d.rect(542,y+51,144,19,'url(#metal)')
  d.poly([(564,y+26),(592,y+51),(564,y+51)],WELD,EDGE)
  if full:d.poly([(542,y+36),(556,y+51),(542,y+65)],WELD,EDGE)
  d.rect(642,y+22,13,62,'#b4c9d9');d.rect(633,y+18,31,12,'#d6e5ee');d.text(513,y+33,label,22)

def beam_intermediate(d):
 d.beam(show_axial=False)
 d.plate(258,-8,0,14,151,174)
 d.seam(256,0,149,256,135,149);d.seam(256,0,12,256,135,12);d.seam(256,55,14,256,55,137)
 d.axial(190)

def flexible_panel(d):
 d.path('M220,142 Q239,170 226,205 Q213,236 229,270 Q244,303 232,340 L258,356 Q265,321 249,282 Q233,243 247,211 Q260,175 243,142 Z',LIGHT)
 d.rect(248,256,286,27,BLUE);d.poly([(248,235),(248,256),(274,256)],WELD,EDGE)
 d.arrow((550,269),(636,269),'Δσ');d.text(315,186,'pannello flessibile',23)
 d.dim((261,232),(287,232),'ℓ')

def planar_attachments(d):
 for trans,kind in [('translate(0,45) scale(.59)','patch'),('translate(350,60) scale(.59)','stud')]:
  d.group(trans);d.attachment(kind);d.end()
 d.text(410,364,'Attacchi piani / pioli non portanti',21,INK,'middle')

def bolted(d,variant):
 if variant=='shear':
  d.rect(195,199,305,35,'url(#metal)');d.rect(195,278,305,35,'url(#metal)');d.rect(350,234,270,44,'url(#metal)')
  d.rect(379,170,35,169,'#b4c9d9');d.rect(361,162,71,23,'#e4edf3');d.rect(361,329,71,23,'#e4edf3')
  for y in range(320,350,6):d.line((379,y),(414,y-5),'#617f92',1)
  d.arrow((188,218),(117,218),'Δτ');d.arrow((188,295),(117,295));d.arrow((625,256),(698,256))
 else:
  for x,head in [(280,True),(485,False)]:
   d.rect(x,155,30,183,'#b4c9d9')
   if head:d.rect(x-20,143,70,24,'#dce9f1')
   for y in range(219 if head else 160,339,7):d.line((x,y),(x+30,y-6),'#617f92',1.1)
   d.dim((x,126),(x+30,126),'d')
   d.arrow((x+15,215),(x+15,178));d.arrow((x+15,266),(x+15,304))

def longitudinal(d,variant):
 if variant in ['i','both','box','manual']:
  d.beam(weld='both' if variant=='both' else 'continuous',box=variant=='box')
 elif variant in ['tee','repair','intermittent','cope']:
  d.beam(tee=True)
  if variant=='intermittent':
   for a,b in [(45,140),(230,330),(410,464)]:d.seam(a,54,14,b,54,14)
   d.dim(d.iso(140,54,70),d.iso(230,54,70),'g');d.dim(d.iso(230,54,70),d.iso(330,54,70),'h')
  elif variant=='cope':
   a=d.iso(270,60,12);d.path(f'M{a[0]-30},{a[1]} a30,30 0 0 1 60,0',LIGHT,INK)
   d.seam(45,54,14,235,54,14);d.seam(305,54,14,465,54,14)
   d.leader((a[0],a[1]-30),(a[0]+45,a[1]-80),'foro di scarico')
  else:
   d.seam(45,54,14,465,54,14)
   if variant=='repair':d.line(d.iso(230,54,14),d.iso(300,54,14),MARK,13);d.leader(d.iso(266,54,14),(445,245),'ripresa',MARK)
 elif variant=='flat':d.plate_joint('long')
 elif variant=='tube':d.tube(seam='long')
 elif variant=='profiles':
  d.group('translate(0,55) scale(.64)');d.beam(weld='continuous');d.end()
  d.group('translate(330,140) scale(.59)');d.beam(weld='continuous',tee=True);d.end()
 else:raise ValueError(variant)

def cross_plan(d,variant):
 if variant in ['radius','radius_aswelded']:
  d.path('M175,230 H255 Q355,230 355,150 V120 H435 V150 Q435,230 535,230 H620 V280 H535 Q435,280 435,370 H355 Q355,280 255,280 H175 Z',LIGHT)
  d.weld((222,230),(222,280),9,variant=='radius');d.weld((573,230),(573,280),9,variant=='radius')
 else:
  d.rect(170,225,450,60,LIGHT);d.rect(350,135,90,230,BLUE)
  for x,s in [(350,-1),(440,1)]:
   if variant!='plain':
    for y,t in [(225,-1),(285,1)]:d.poly([(x,y),(x+s*72,y),(x,y+t*65)],LIGHT)
   d.weld((x,213),(x,297),9,variant=='ground')
 d.arrow((165,255),(93,255),'Δσ');d.arrow((628,255),(700,255))

def truss(d,variant):
 d.rect(175,288,450,76,LIGHT)
 d.line((175,301),(625,301),INK,1.3,'9 6');d.line((175,350),(625,350),INK,1.3,'9 6')
 overlap=variant in ['overlap','n'];left=392 if overlap else 350;right=383 if overlap else 450
 if variant=='n':d.poly([(275,149),(328,149),(328,288),(275,288)],BLUE)
 else:d.poly([(180,152),(225,125),(left+15,288),(left-48,288)],BLUE)
 d.poly([(570,127),(610,158),(right+47,288),(right-19,288)],BLUE)
 d.weld((left-47 if variant!='n' else 275,288),(left+13 if variant!='n' else 328,288))
 d.weld((right-18,288),(right+47,288))
 if not overlap:d.dim((left+15,257),(right-19,257),'g')
 d.arrow((260,183),(225,145));d.arrow((560,188),(595,150))
 d.dim((660,288),(660,364),'b₀' if variant=='rect' else 'd₀')
 d.text(400,393,'Nodi K / N · elementi cavi',20,INK,'middle')

def deck(d,variant):
 if variant in ['splice','splice_backed']:
  # Folded trapezoidal rib, with an actual cross-rib seam.
  def section(x):return [(x,0,120),(x,35,10),(x,105,10),(x,140,120)]
  a=section(90);b=section(460)
  for i in range(3):d.face([a[i],b[i],b[i+1],a[i+1]],LIGHT if i==1 else BLUE)
  s=section(280)
  for i in range(3):d.seam(*s[i],*s[i+1])
  if variant=='splice_backed':d.text(390,136,'con sostegno al rovescio',21,INK,'middle')
  d.axial(25,-90)
 else:
  d.rect(170,150,460,24,'url(#metal)')
  d.path('M285,174 L330,326 Q334,337 348,337 H452 Q466,337 470,326 L515,174 L499,174 L456,316 Q452,322 445,322 H355 Q348,322 344,316 L301,174 Z',LIGHT)
  d.poly([(285,174),(307,174),(308,200)],WELD,EDGE);d.poly([(515,174),(493,174),(492,200)],WELD,EDGE)
  if variant=='backed':d.path('M310,273 L325,322 Q331,350 353,350 H447 Q469,350 475,322 L490,273',stroke=SIDE,width=9)
  if variant=='intersection':
   d.path('M240,220 H276 Q284,260 315,273 M560,220 H524 Q516,260 485,273',stroke=INK,width=3)
   d.text(280,244,'A',23);d.text(506,244,'A',23)
  d.arrow((140,162),(80,162),'Δσ')
  d.text(400,382,'Nervatura trapezoidale / lamiera',21,INK,'middle')

def rib_root(d,variant):
 d.rect(170,177,460,32,'url(#metal)')
 d.poly([(348,209),(375,209),(428,356),(401,366)],'url(#metal)')
 if variant in ['full','iiwfull']:
  d.poly([(329,177),(379,177),(389,244),(353,218)],WELD,EDGE)
 else:d.poly([(313,209),(350,209),(370,260)],WELD,EDGE);d.line((350,209),(361,217),MARK,3)
 d.dim((463,319),(434,330),'t');d.leader((345,215),(257,279),'a',EDGE)
 d.arrow((170,154),(117,129),'Mℓ');d.arrow((633,154),(686,129),'Mr');d.arrow((455,360),(508,380),'Mw')

def gusset_profile(d,variant):
 d.rect(200,279,450,49,LIGHT)
 if variant=='round':d.path('M205,138 Q216,251 397,252 L421,279 H205 Z',BLUE)
 else:d.path('M205,143 L415,247 Q423,255 425,279 H205 Z',BLUE)
 d.weld((211,277),(420,277));d.dim((200,355),(420,355),'L')
 d.arrow((185,303),(115,303),'Δσ');d.arrow((660,303),(728,303))
 d.dim((447,253),(447,279),'c');d.dim((677,279),(677,328),'h')
 d.leader((395,252),(485,187),'r');d.text(265,229,'φ',24)

def flat_gusset(d,variant):
 d.plate()
 if variant=='radius':
  d.path('M280,325 Q300,355 340,359 L365,359 Q405,358 410,325 Z',BLUE)
  d.weld((285,325),(405,325),8,True);d.leader((307,349),(225,382),'r')
 else:d.plate(175,-80,0,190,80,12);d.seam(175,0,12,365,0,12)
 d.axial(40)

def flattened(d,variant):
 # Plan and elevation: the opening/slit is deliberately visible.
 if variant=='butt':
  d.path('M175,145 H300 L415,173 L420,188 L300,218 H175 Z',LIGHT);d.rect(420,173,215,15,LIGHT);d.weld((417,172),(417,190),8)
  d.path('M175,284 H290 Q348,284 416,313 L635,313 L635,325 L416,325 Q348,354 290,354 H175 Z',LIGHT)
  d.weld((417,313),(417,325),8)
 else:
  d.path('M175,151 H455 V175 H377 Q350,175 350,187 Q350,199 377,199 H455 V223 H175 Z',LIGHT)
  d.rect(379,179,255,16,BLUE);d.weld((380,177),(455,177),7);d.weld((380,197),(455,197),7)
  d.rect(175,315,270,12,BLUE);d.path('M445,283 Q350,283 280,309 L175,309 V334 H280 Q350,359 445,359 Z',LIGHT)
  d.weld((295,309),(433,309),7);d.weld((295,334),(433,334),7)
 d.arrow((167,187),(95,187),'Δσ');d.arrow((640,187),(712,187))

def concentrated(d):
 d.beam(weld='continuous',show_axial=False)
 d.path('M337,114 A70,60 0 0 0 477,114',fill=LIGHT)
 d.arrow((407,113),(407,155),'F')
 d.dim(d.iso(210,-22,160),d.iso(360,-22,160),'b')

def curved(d,variant):
 if variant=='knuckle':
  d.poly([(170,153),(335,254),(627,254),(627,277),(326,277),(157,172)],LIGHT)
  d.poly([(331,277),(331,360),(360,360),(360,277)],BLUE);d.weld((327,277),(362,277))
  d.arrow((211,178),(145,137),'Ff');d.arrow((549,265),(680,265),'Ff');d.arrow((345,301),(345,370),'Fst')
 else:
  d.path('M170,157 Q360,326 633,245 L641,269 Q360,353 158,176 Z',LIGHT)
  d.path('M197,207 Q372,335 605,291 L605,370 H197 Z',BLUE)
  d.path('M197,207 Q372,335 605,291',stroke=WELD,width=9)
  for x,y in [(250,245),(310,275),(380,297),(454,304),(530,302)]:d.arrow((x,y),(x-4,y+40))
  d.arrow((216,201),(152,149),'Ff');d.arrow((571,263),(650,243),'Ff');d.text(411,201,'r',24)

def render(spec):
 d=Drawing();f=spec['family'];v=spec.get('variant','');opts=spec.get('options',{})
 if f=='plate':
  d.plate_joint(v or 'plain')
  if v.startswith('cut'):
   for x in range(45,470,15):d.line(d.iso(x,0,0),d.iso(x+4,0,10),SIDE,1.5)
 elif f=='beam':
  d.beam(holes=v=='holes',cover=v=='cover',show_axial=v!='shear')
  if v=='shear':d.arrow((310,246),(390,246),'Δτ');d.arrow((390,269),(310,269))
 elif f=='tube':
  d.tube(rect=v=='rect',seam='long' if v=='long' else None,collar=v=='ring',show_axial=v!='shear')
  if v=='shear':d.arrow((290,262),(380,252),'Δτ');d.arrow((380,279),(290,289))
 elif f=='bolted':bolted(d,v)
 elif f=='longitudinal':longitudinal(d,v)
 elif f=='butt':
  if v in ['section','v','partial','backed','offset','threeplate','step']:
   d.butt_section(style='v' if v in ['v','backed','threeplate'] else 'x',partial=v=='partial',backing=v=='backed',offset=v=='offset',step=v=='step',**opts)
   if v=='threeplate':d.rect(378,276,44,75,'url(#metal)')
  else:
   d.plate_joint('one_sided' if v=='one_sided' else 'butt',flush=v=='flush')
   if v in ['flush','cap01','cap02','root']:
    d.group('translate(200,20) scale(.50)');d.butt_section(flush=v=='flush',style='v' if v=='root' else 'x');d.end()
    if v.startswith('cap'):d.text(400,196,'h ≤ 0,'+v[-1]+' b',21,EDGE,'middle')
 elif f=='beam_splice':d.beam(butt=v or 'all')
 elif f=='transition':transition(d,v)
 elif f=='attachment':d.attachment(kind=v if v not in ['taper','radius'] else 'long',taper=v=='taper',rounded=v=='radius',**opts)
 elif f=='gusset':gusset_profile(d,v)
 elif f=='flat_gusset':flat_gusset(d,v)
 elif f=='stiffeners':
  d.beam(box=v=='box')
  if v=='box':d.plate(290,12,13,8,116,124);d.seam(285,12,13,285,12,135)
  else:
   for x in [180,365]:d.plate(x,4,12,9,54,125);d.seam(x,0,13,x,54,13);d.seam(x,0,13,x,0,135)
 elif f=='cruciform':d.cross_section(partial=v in ['partial','singlepartial'],single=v in ['single','singlepartial'],nonload=v=='nonload',ground=v=='ground')
 elif f=='lap':
  if v in ['double','section']:d.lap_section(double=v=='double')
  else:
   d.plate();d.plate(200,22,12,210,90,12)
   d.seam(200,22,24,410,22,24);d.seam(200,112,24,410,112,24)
   if v!='side':d.seam(410,22,24,410,112,24)
   if v=='reinforced':d.seam(410,22,24,445,112,14)
   d.axial(42)
 elif f=='runway':d.runway(int(v),load=opts.get('load',True))
 elif f=='tube_section':d.tube_section(v or 'round',**opts)
 elif f=='flange':d.flange_section(**opts)
 elif f=='flat_tube':flattened(d,v)
 elif f=='cross_plan':cross_plan(d,v)
 elif f=='truss':truss(d,v)
 elif f=='deck':deck(d,v)
 elif f=='rib_root':rib_root(d,v)
 elif f=='curved':curved(d,v)
 elif f=='wheel':concentrated(d)
 elif f=='block':
  d.rect(200,185,200,150,'url(#metal)');d.rect(400,245,245,57,'url(#metal)')
  d.poly([(400,225),(430,245),(400,270)],WELD,EDGE)
  if v=='full':d.poly([(400,270),(430,302),(400,322)],WELD,EDGE)
  else:d.line((400,267),(400,300),MARK,3)
  d.arrow((650,272),(715,272),'Δσ')
 elif f=='tube_solid':
  d.rect(170,208,260,104,LIGHT);d.rect(170,222,240,76,'white');d.rect(430,208,210,104,'url(#metal)')
  d.weld((420,208),(451,208),9);d.weld((420,312),(451,312),9);d.arrow((161,262),(87,262),'Δσ');d.arrow((651,262),(724,262))
 elif f=='reinforced_tube':d.tube(rect=True);d.plate(185,40,100,190,53,12);d.seam(185,40,113,375,40,113);d.seam(375,40,113,375,93,113)
 elif f=='beam_tee':
  d.beam();d.plate(270,0,149,240,135,12);d.seam(270,0,162,270,135,162);d.dim(d.iso(270,0,185),d.iso(510,0,185),'L')
 elif f=='hollow_attachment':hollow_attachment(d)
 elif f=='bolted_flange':bolted_flange(d)
 elif f=='beam_intermediate':beam_intermediate(d)
 elif f=='flexible_panel':flexible_panel(d)
 elif f=='planar_attachments':planar_attachments(d)
 elif f=='profiles':
  for tr,fam,var in [('translate(20,45) scale(.49)','plate',''),('translate(405,35) scale(.49)','beam',''),('translate(0,245) scale(.44)','tube',''),('translate(415,230) scale(.44)','tube','rect')]:
   d.group(tr)
   if fam=='plate':d.plate_joint('plain')
   elif fam=='beam':d.beam()
   else:d.tube(rect=var=='rect')
   d.end()
 else:raise ValueError(f'Unknown diagram family: {f}')
 return d
