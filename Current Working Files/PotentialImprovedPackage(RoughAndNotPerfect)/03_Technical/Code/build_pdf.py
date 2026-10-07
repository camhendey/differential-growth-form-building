"""Build the editorial project record from saved evidence, metrics and renders."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from PIL import Image

ROOT=Path(__file__).resolve().parents[2];VIS=ROOT/'02_Visuals';DATA=ROOT/'03_Technical/Data'
OUT=ROOT/'01_Portfolio/STRIA_Master_Case_Study.pdf'
W,H=1100,760
INK='#14262F';PAPER='#F6F3EC';MUTED='#52636A';CORAL='#C45C43';BLUE='#245BE0';LINE='#D8DBD6'
for name,file in [('Sans','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(name,str(VIS/'Fonts'/file)))
MET=json.loads((DATA/'metrics.json').read_text());VAL=json.loads((DATA/'validation.json').read_text())
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('STRIA | Controlled growth for porous space');c.setAuthor('Cameron Hendey');c.setSubject('Computational design system, design studies and technical evidence')
PAGE=0;BG=PAPER

def rect(x,y,w,h,color):
    c.setFillColor(HexColor(color));c.rect(x,H-y-h,w,h,fill=1,stroke=0)
def text(s,x,y,size=14,color=INK,font='Sans'):
    c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,H-y-size*.82,s)
def para(s,x,y,w,size=14,color=INK,leading=None):
    style=ParagraphStyle('p',fontName='Sans',fontSize=size,leading=leading or size*1.5,textColor=HexColor(color),spaceAfter=0)
    p=Paragraph(s,style);_,h=p.wrap(w,H);p.drawOn(c,x,H-y-h)
    assert y+h<710,('Text outside content area',PAGE,s[:60],y+h)
    return h
def image(name,x,y,w,h,fill=False):
    p=VIS/name;im=Image.open(p);iw,ih=im.size;scale=max(w/iw,h/ih) if fill else min(w/iw,h/ih);ww,hh=iw*scale,ih*scale
    c.saveState();path=c.beginPath();path.rect(x,H-y-h,w,h);c.clipPath(path,stroke=0);c.drawImage(str(p),x+(w-ww)/2,H-y-h+(h-hh)/2,ww,hh,mask='auto');c.restoreState()
def line(x1,y1,x2,y2,color=LINE,width=1):
    c.setStrokeColor(HexColor(color));c.setLineWidth(width);c.line(x1,H-y1,x2,H-y2)
def new(section,title=None,subtitle=None,dark=False):
    global PAGE,BG
    if PAGE:c.showPage()
    PAGE+=1;BG=INK if dark else PAPER;rect(0,0,W,H,BG)
    c.bookmarkPage(f'p{PAGE}');c.addOutlineEntry(section+(' / '+title if title else ''),f'p{PAGE}',0)
    text('STRIA',52,28,13,CORAL,'Bold');text(section.upper(),150,29,10,'#CDD5D8' if dark else MUTED,'Mono')
    if title:text(title,52,80,34,'#FFFFFF' if dark else INK,'Bold')
    if subtitle:para(subtitle,54,133,990,14,'#CDD5D8' if dark else MUTED)
    line(52,717,1048,717,'#3A4B52' if dark else LINE)
    text('CAMERON HENDEY  /  COMPUTATIONAL DESIGN',52,731,9,'#CBD4D8' if dark else MUTED,'Mono');text(f'{PAGE:02d}',1025,730,11,'#CBD4D8' if dark else MUTED,'Mono')
def label(s,x,y):text(s.upper(),x,y,10,CORAL,'Mono')
def item(title,body,x,y,w=290,color=INK):
    text(title,x,y,18,color,'Bold');return para(body,x,y+32,w,14,MUTED if color==INK else '#CDD5D8')
def stat(value,caption,x,y,w=290):
    text(value,x,y,42,CORAL,'Bold');para(caption,x,y+57,w,13,MUTED)
def node(title,body,x,y,w=210,h=100):
    rect(x,y,w,h,'#223A45');text(title,x+16,y+16,16,'#FFFFFF','Bold');para(body,x+16,y+43,w-32,12,'#CDD5D8')
def arrow(x1,y1,x2,y2,color=CORAL):
    line(x1,y1,x2,y2,color,2)
    import math
    a=math.atan2(y2-y1,x2-x1)
    for off in [-.5,.5]:line(x2,y2,x2-8*math.cos(a+off),y2-8*math.sin(a+off),color,2)

new('Project record')
image('Showcase_Courtyard.png',0,0,W,H,fill=True)
text('STRIA',52,62,82,INK,'Bold')
text('Growth becomes space.',57,163,23,INK)
text('TORQUED CRESCENT / COMPUTATIONAL FORM',58,209,10,MUTED,'Mono')
rect(0,711,1100,49,PAPER)
text('CAMERON HENDEY',54,731,10,INK,'Mono')
text('Interpretive architectural collage / model geometry documented inside',422,733,10,MUTED)

new('Overview','A field of curves. A place to enter.','Differential growth developed from a controlled screen study into a flared, twisting spatial enclosure.')
para('The torqued crescent turns a porous pattern into an inhabitable form. Four closed growth loops follow a shared envelope, wrapping around an open interior and drawing the eye along a diagonal entrance.',54,205,425,18,INK,27)
image('crescent_render.png',525,173,550,450)
stat('280°','Crescent sweep with an open entrance.',54,427,210)
stat('38°','Rotation from lower to upper edge.',298,427,210)
para('The showcase explores spatial form. The cylindrical benchmark on pages 5-8 retains the measured field comparison and its original results.',54,572,440,13)
line(54,630,1046,630)
for x,num,txt in [(54,3,'Source + system'),(310,7,'Benchmark evidence'),(566,9,'Spatial application'),(822,14,'Method + verification')]:
    text(f'{num:02d}',x,654,22,CORAL,'Bold');text(txt,x+44,661,12);c.linkRect('',f'p{num}',(x,H-689,x+230,H-650),relative=0)

new('Design intent','Separate the envelope from the pattern.','One controls overall spatial form. The other controls the distribution of a connected strand.')
image('original.png',52,190,480,435)
label('Evidence: source form study',54,645)
para('Render of supplied mesh, normalized for display only. Its original physical units are unspecified.',54,666,460,12)
item('The envelope','A host surface establishes silhouette and spatial extent. In the source definition, profile manipulation and lofting create a twisting envelope.',590,206,440)
item('The pattern','A curve expands under length, bending and collision constraints. The growth pattern occupies the surface without defining its entire silhouette.',590,365,440)
item('The application','A curved screen establishes a measurable benchmark. The crescent extends that pattern into a twisting enclosure, exploring volume, thresholds and layered views.',590,523,440)

new('System architecture','A legible chain of decisions.','Geometry, control and evaluation remain separate enough to inspect and change.',dark=True)
node('Host surface','Width, height and curvature',54,219)
node('Seed curve','Closed loop + deterministic perturbation',54,355)
node('Spacing field','Uniform, height gradient or focused',54,491)
node('Growth solver','Expansion + repulsion + smoothing',398,330,248,116)
node('Fair + map','Resample; benchmark or crescent map',758,219,285)
node('Measure','Benchmark checks; crescent size + stretch',758,355,285)
node('Export','Centerline + mesh + native Rhino model',758,491,285)
arrow(264,269,398,365);arrow(264,405,398,387);arrow(264,541,398,411)
line(646,385,705,385,CORAL,2);line(705,385,705,269,CORAL,2);arrow(705,269,758,269)
arrow(900,319,900,355);arrow(900,455,900,491)
para('Evaluation informs selection. The solver does not automatically optimize these metrics, and a completed iteration budget is not evidence of convergence.',398,519,287,13,'#CDD5D8')

new('Benchmark / controls','Local rules, visible consequences.','The field changes exclusion distance. It does not prescribe an openness percentage.')
image('fields.png',52,182,995,318)
for x,title,body in [(54,'Uniform','A constant 30 mm spacing target.'),(393,'Gradient','A 30-56 mm spacing target increasing with height.'),(731,'Focused','A smooth 30-56 mm field centred around the viewing band.')]:item(title,body,x,525,290)
line(54,642,1046,642)
para('All three studies use the same seed, enclosure, iteration budget, node limit, final strand diameter and evaluation method. The nominal spacing target is a soft repulsion distance, not a guaranteed finished gap.',54,662,984,13)

new('Benchmark / process','Growth is recorded, not reconstructed.','Saved simulation states show how a simple loop develops folds and occupies the domain.')
image('growth_sequence.png',40,200,1020,293)
item('01 / Expansion','Neighbor segments seek a 27 mm length. Together with repulsion and bending, this drives local expansion and folding.',54,529,292)
item('02 / Refinement','Long edges are split in bounded batches. The design studies stop at 3,500 nodes and 6,500 growth iterations.',395,529,292)
item('03 / Fairing','Index-space smoothing is followed by equal-arclength resampling and light Gaussian fairing. All reported checks use the resulting geometry.',735,529,292)

new('Benchmark / comparison','Three settings. One comparison protocol.','Dashed green boxes mark the same 0.5 x 0.5 m viewing zone in every front projection.')
image('comparison.png',52,180,555,490)
rows=[['Measure','Uniform','Gradient','Focused'],['Zone open',*[f"{MET[n]['view_zone_open_fraction']*100:.1f}%" for n in MET]],['Whole panel open',*[f"{MET[n]['front_open_fraction']*100:.1f}%" for n in MET]],['Path length',*[f"{MET[n]['path_length_m']:.2f} m" for n in MET]],['Min. nonlocal distance',*[f"{MET[n]['minimum_nonlocal_centerline_distance_m']*1000:.1f} mm" for n in MET]],['Tight-bend flags',*[str(MET[n]['bend_radius_below_strand_radius_vertices']) for n in MET]]]
xs=[635,820,900,981];y=219
for r,row in enumerate(rows):
    if r==0:rect(622,y-12,425,39,INK)
    for j,cell in enumerate(row):text(cell,xs[j],y,11 if j else 11,'#FFFFFF' if r==0 else INK,'Bold' if r==0 else 'Sans')
    if r:line(630,y+29,1045,y+29)
    y+=60
para('The uniform study keeps a dense central region and retains ten sampled bend-radius flags at the chosen 9 mm diameter. Watertight topology alone would not reveal that limitation.',632,609,409,13)

new('Benchmark / selection','Choose the field, not the longest path.','The focused study balances an open viewing band, a legible organic pattern and fewer geometric conflicts.')
stat('28.20 m','Centerline length in the selected screen.',54,209)
stat('21.3 mm','Minimum checked nonlocal centerline distance.',395,209)
stat('5.48 mm','Minimum sampled bend radius; strand radius is 4.5 mm.',735,209)
line(54,370,1046,370)
item('Why not uniform?','Its viewing-zone openness is lower and its tightest bends are smaller than the proposed strand radius. It remains useful as a baseline, not the selected geometry.',54,409,295)
item('Why not gradient?','It passes the sampled bend check and opens the viewing zone, but uses a longer path. The focused variant uses 12.4% less centerline length with slightly higher zone openness.',395,409,295)
item('What this does not prove','Shorter centerline length is not a verified material or cost saving. The study does not include joining losses, supports, manufacturing allowances or load requirements.',735,409,295)
para('Selection combines measured trade-offs and design judgment. No claim of a global optimum is made.',54,639,980,16,CORAL)

new('Spatial application','A crescent shaped by flare and torque.','Exact model render. The envelope defines the space; four mapped growth loops articulate its surface.')
image('crescent_render.png',333,182,725,510)
para('A widening radius and rotating section turn a simple arc into a dynamic shell. The open edge becomes an entrance, while the flared rim gives the object a distinctive silhouette.',54,208,265,18,INK,27)
label('Modeled strand envelope',54,450)
para('4.13 x 4.21 x 2.91 m<br/>198.45 m total centerline<br/>4 closed loops / 14,000 nodes<br/>16 mm strand diameter',54,481,270,14)
para('Envelope values bound strand centerlines, excluding the perimeter. Dimensions are design proposals.',54,614,270,12)

new('Benchmark / assembly','Make connections explicit.','Concept mounting ties connect the growth curve to the perimeter instead of leaving the strand visually unsupported.')
image('detail.png',52,184,650,485)
item('Modeled assembly','The native Rhino file separates the growth strand, perimeter frame and six concept mounting ties into named layers.',742,210,290)
item('Unresolved engineering','Tie dimensions, joint type, frame stiffness and base stability are not mechanically verified. The render communicates arrangement, not a build specification.',742,395,290)
para('A watertight strand mesh is an exchangeable digital object. It is not proof that a single unsupported strand can hold this shape physically.',742,592,290,13,CORAL)

new('Spatial experience','An interior made from lines.')
image('Showcase_Interior.png',0,151,1100,550,fill=True)
rect(52,650,997,42,PAPER)
para('Interpretive AI-assisted collage: atmosphere, finish, figures and context are illustrative. Exact geometry is recorded in the model views.',65,661,960,11)

new('Envelope logic','One surface. Four growth domains.','The selected benchmark curve is repeated across four adjacent parameter regions, then mapped into the crescent.')
image('crescent_atlas.png',30,158,1040,424)
item('Silhouette','A 280° plan arc leaves an entrance. Radius increases with height; the upper edge rotates by 38° and varies in elevation.',54,561,297)
item('Surface articulation','Four independent closed curves produce a denser wrapping pattern. Their placement follows the same host function.',395,561,297)
item('Mapping trade-off','Local segment lengths stretch by 1.19-2.80x. This is a form study, not a fresh growth simulation on the curved surface.',735,561,297)

new('Showcase / courtyard')
image('Showcase_Courtyard.png',0,60,1100,650,fill=True)
rect(52,91,315,85,PAPER)
text('TORQUED CRESCENT',68,109,17,INK,'Bold')
text('A porous room in the landscape.',68,140,13,MUTED)
rect(52,675,997,29,PAPER)
text('Interpretive collage / proportions, context and shadows are artistic; refer to model for dimensions.',64,684,10,MUTED)

new('Benchmark / method','A surface mapping with an explicit contract.','A cylindrical test surface makes the relationship between the planar solver and three-dimensional output inspectable.')
image('elevation.png',54,187,430,480)
label('Coordinate mapping',546,207)
text('x = R sin(u / R)',546,241,23,INK,'Mono');text('y = R [1 - cos(u / R)]',546,281,23,INK,'Mono');text('z = v',546,321,23,INK,'Mono')
para('The two parameter directions have unit length and are perpendicular. The unrolled domain therefore preserves intrinsic distances on the cylinder. This is not a general solution for arbitrary doubly curved surfaces.',546,379,485,15)
para('Nonlocal distance checks use the exported 3D polyline, not only distances in the unrolled plane. Surface-deviation checks evaluate centerline vertices. Straight chords between vertices and the swept strand have finite geometric offsets.',546,499,485,14)
para('The Python implementation is independent of Kangaroo. Numerical equivalence with the archived Grasshopper simulation has not been established.',546,632,485,13,CORAL)

new('Benchmark / verification','Test what the evidence can actually support.','Verification is attached to saved geometry and exact configurations, not inferred from the renders.')
checks=[('7 / 7','Unit tests pass','Cylinder membership, intrinsic metric, field bounds, segment-distance cases, cyclic mesh closure and short-run determinism.'),('Exact','Full-run replay','Seed 17 was rerun for 6,500 iterations. Final coordinates match the saved selected output exactly in this environment.'),('0','Nonlocal clearance flags','59,797 candidate segment pairs checked for the focused study. Pairs within 50 mm of path arclength are excluded.'),('0','Sampled tight-bend flags','No focused-study vertex has a discrete bend radius below the proposed 4.5 mm strand radius.')]
for i,(value,title,body) in enumerate(checks):
    y=200+i*115;text(value,54,y,32,CORAL,'Bold');text(title,223,y+1,19,INK,'Bold');para(body,223,y+35,795,13)
para('An additional seed-29 run is retained in the technical package. One alternative seed is a sensitivity probe, not a statistical robustness study. Full swept-mesh self-intersection and physical tests remain outstanding.',54,665,990,12,MUTED)

new('Reproduction','A project record that can be rerun.','The package contains source code, input evidence, saved states, measurements, native geometry and editable graphics.')
left=[('01 / Run the model','growth.py reproduces the three named studies and saves UV coordinates, XYZ coordinates, state snapshots and a configuration manifest.'),('02 / Inspect and export','analyze_export.py calculates the geometric measures and writes PLY, OBJ and native Rhino files with separate assembly layers.'),('03 / Verify the result','tests.py checks core functions. validate.py replays the selected full run and records one alternate seed.'),('04 / Rebuild presentation','figures.py produces study graphics. showcase.py exports the crescent and its atlas. render_crescent.py renders its meshes. build_pdf.py assembles this document.')]
for i,(t,b) in enumerate(left):item(t,b,54,203+i*117,520)
rect(631,194,413,450,INK)
text('Native Grasshopper recovery',651,221,20,'#FFFFFF','Bold')
para('The original definition is preserved. A separate repaired copy reconnects the final curve to Pipe, enables the output branch and requests periodic curve construction.',651,272,367,14,'#CDD5D8')
para('The binary serializer was verified against the original decompressed bytes before editing. This checks file preservation, not runtime correctness.',651,391,367,14,'#CDD5D8')
para('Native Rhino/Kangaroo execution and solver vertex-order verification remain necessary. Do not treat the repair as a confirmed reproduction of the supplied final mesh.',651,509,367,14,'#F0B6A6')

new('Boundaries','A credible digital study has visible limits.','The benchmark is tested. The crescent is a geometric extension; physical realization remains unverified.')
columns=[('Implemented',['Deterministic growth solver','Three controlled design studies','Local spacing field','Adaptive refinement + fairing','Geometry checks and replay','Native models + crescent mapping']),('Proposed',['Non-load-bearing screen','1.80 m benchmark height','Copper-toned finish','Perimeter and mounting ties','Freestanding supports','Torqued crescent installation']),('Not established',['Structural adequacy','Material performance or savings','Toolpath or nozzle access','Fabrication time and cost','Daylight or acoustic performance','Kangaroo numerical equivalence'])]
for i,(title,items) in enumerate(columns):
    x=54+i*341;text(title,x,217,23,CORAL if i==2 else INK,'Bold')
    for j,s in enumerate(items):line(x,280+j*48,x+292,280+j*48);text(s,x,294+j*48,13)
para('The crescent needs new clearance and curvature checks, joint design and structural development. Benchmark openness and clearance results must not be transferred to this non-isometric host.',54,645,980,16)

new('Evidence + attribution','Every major claim has a traceable source.','Supporting records preserve the distinction between supplied evidence, newly computed results and conceptual application.')
item('Source evidence','ARC3201 Project 3 archive, December 2024: research paper, 22-slide presentation and Grasshopper definition. Additional evidence: supplied final mesh, three four-view screenshots and a 36.3-second growth recording.',54,199,480)
item('Authorship','Cameron Hendey independently developed the original Grasshopper script, informed by existing differential-growth examples. The redevelopment code, analysis, renders and documentation were produced with AI assistance under his approved scope.',54,393,480)
item('Computational evidence','run_manifest.json records conditions; metrics.json records comparisons; validation.json records tests and replay; the NPZ files contain final coordinates and saved growth states. showcase_metrics.json records the crescent separately. The two artistic collages interpret the model; they are not measurement evidence. Original files remain unchanged.',591,199,450)
label('External context',591,403)
para('ZHA, <i>Thallus Installation</i> (2017). Relevant precedent for surface-constrained growth and continuous robotic deposition. The precedent is not evidence of this project\'s fabrication capability.',591,432,450,13)
para('<link href="https://www.zha.com/projects/installations-pavilions/thallus-installation?disclaimer=true" color="#245BE0">Official Thallus project description</link>',591,515,450,12)
para('McNeel, GH_IO documentation. Used to interpret archive types and serialization. Component metadata and connectivity were read from the actual supplied file.',591,558,450,13)
para('<link href="https://developer.rhino3d.com/api/grasshopper/html/T_GH_IO_Types_GH_Types.htm" color="#245BE0">Grasshopper GH_IO type documentation</link>',591,639,450,12)
c.save();print('Created',OUT,'pages',PAGE)
