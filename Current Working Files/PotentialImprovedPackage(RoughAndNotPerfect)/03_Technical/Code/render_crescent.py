"""Exact mesh render for crescent geometry. Artistic collages are separate."""
from pathlib import Path
import mitsuba as mi
mi.set_variant('llvm_ad_rgb')
from render import box,mesh,matte,metal,T
ROOT=Path(__file__).resolve().parents[2];M=ROOT/'03_Technical/Models';V=ROOT/'02_Visuals'
d={'type':'scene','integrator':{'type':'path','max_depth':5,'hide_emitters':True},'sensor':{'type':'perspective','fov':37,'to_world':T.look_at(origin=[-6,-10,6],target=[0,0,1.6],up=[0,0,1]),'sampler':{'type':'independent','sample_count':32},'film':{'type':'hdrfilm','width':2000,'height':1600}},'env':{'type':'constant','radiance':{'type':'rgb','value':[.6,.65,.7]}},'floor':box([0,0,-.08],[200,200,.15],matte([.79,.76,.69])),'light':{'type':'rectangle','to_world':T.look_at(origin=[-3,-4,7],target=[0,0,1],up=[0,0,1])@T.scale([3,3,1]),'emitter':{'type':'area','radiance':{'type':'rgb','value':[5,4.4,3.6]}}}}
for i in range(4):d[f'curve{i}']=mesh(M/f'crescent_strand_{i}.ply',metal([.38,.12,.055]))
d['frame']=mesh(M/'crescent_frame.ply',metal([.07,.085,.07]))
s=mi.load_dict(d);im=mi.render(s,spp=48,seed=17);mi.util.write_bitmap(str(V/'crescent_render.png'),im);print('Rendered crescent')
