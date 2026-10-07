"""Path-traced images from exported mesh geometry using Mitsuba 3."""
from pathlib import Path
import argparse
import numpy as np
import mitsuba as mi
mi.set_variant('llvm_ad_rgb')
ROOT=Path(__file__).resolve().parents[2]
MODELS=ROOT/'03_Technical/Models';OUT=ROOT/'02_Visuals'
T=mi.ScalarTransform4f

def matte(rgb):return {'type':'diffuse','reflectance':{'type':'rgb','value':rgb}}
def metal(rgb,rough=.28):return {'type':'roughplastic','diffuse_reflectance':{'type':'rgb','value':rgb},'alpha':rough,'int_ior':1.49}
def box(pos,size,mat):return {'type':'cube','to_world':T.translate(pos)@T.scale(np.array(size)/2),'bsdf':mat}
def mesh(file,mat,transform=None):
    d={'type':'ply','filename':str(file),'bsdf':mat,'face_normals':False}
    if transform is not None:d['to_world']=transform
    return d

def scene(kind='studio',resolution=1800):
    coral=metal([.60,.18,.10]);bronze=metal([.45,.25,.10]);ink=metal([.036,.047,.053]);white=matte([.74,.73,.68])
    cam=[2.7,-4.2,2.5];target=[0,.03,.90];fov=32;aspect=1.2
    if kind=='detail':cam=[.78,-1.15,1.36];target=[.12,.045,1.05];fov=26;aspect=1.25
    if kind=='hero':cam=[4.9,-7.6,3.4];target=[0,.18,.86];fov=35;aspect=1.6
    if kind=='original':cam=[1.6,-2.4,1.6];target=[0,0,.5];fov=32;aspect=1.2
    d={'type':'scene','integrator':{'type':'path','max_depth':7},'sensor':{'type':'perspective','fov':fov,'to_world':T.look_at(origin=cam,target=target,up=[0,0,1]),'sampler':{'type':'independent','sample_count':80},'film':{'type':'hdrfilm','width':resolution,'height':int(resolution/aspect),'rfilter':{'type':'tent'}}},'environment':{'type':'constant','radiance':{'type':'rgb','value':[.25,.28,.33]}},'floor':box([0,0,-.085],[200,200,.15],white),'key':{'type':'rectangle','to_world':T.look_at(origin=[-2,-3,5],target=[0,0,.7],up=[0,0,1])@T.scale([2,2,1]),'emitter':{'type':'area','radiance':{'type':'rgb','value':[8,7.2,6.1]}}}}
    if kind=='original':
        d['object']=mesh(MODELS/'original_display_normalized.ply',bronze)
        d['plinth']=box([0,0,-.025],[1.1,.9,.05],ink)
    else:
        d['strand']=mesh(MODELS/'focused_strand.ply',coral)
        d['frame']=mesh(MODELS/'frame.ply',ink)
        d['ties']=mesh(MODELS/'focused_ties.ply',ink)
        for i,x in enumerate([-.48,.48]):d[f'foot{i}']=box([x,.06,.012],[.065,.48,.024],ink)
        if kind=='hero':
            for k,(x,angle) in enumerate([(-1.29,-12),(1.29,12)]):
                trans=T.translate([x,.20,0])@T.rotate([0,0,1],angle)
                d[f'strand{k}']=mesh(MODELS/'focused_strand.ply',coral,trans)
                d[f'frame{k}']=mesh(MODELS/'frame.ply',ink,trans)
                d[f'ties{k}']=mesh(MODELS/'focused_ties.ply',ink,trans)
                for j,xx in enumerate([-.48,.48]):
                    b=box([0,0,0],[.065,.48,.024],ink);b['to_world']=trans@T.translate([xx,.06,.012])@T.scale([.0325,.24,.012]);d[f'foot{k}{j}']=b
            # Architectural context is a conceptual gallery, not a built site.
            d['wall']=box([0,2.5,2.2],[14,.16,4.5],matte([.76,.76,.73]))
            d['bench']=box([-1.65,1.5,.4],[1.35,.45,.08],matte([.30,.17,.08]))
            for i,x in enumerate([-2.1,-1.2]):d[f'benchleg{i}']=box([x,1.5,.2],[.05,.36,.4],ink)
            d['sun']={'type':'directional','direction':[.65,.70,-1],'irradiance':{'type':'rgb','value':[2.5,2.1,1.7]}}
    return d

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--kind',default='studio');ap.add_argument('--resolution',type=int,default=1800);ap.add_argument('--spp',type=int,default=96);a=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    s=mi.load_dict(scene(a.kind,a.resolution));im=mi.render(s,spp=a.spp,seed=17)
    mi.util.write_bitmap(str(OUT/f'{a.kind}.png'),im)
    print('Rendered',a.kind,flush=True)

if __name__=='__main__':main()
