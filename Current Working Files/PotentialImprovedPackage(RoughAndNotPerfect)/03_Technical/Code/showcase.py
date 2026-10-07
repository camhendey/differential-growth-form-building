"""Torqued crescent: geometric extension of the saved focused growth curve.
Mapping is not isometric and does not constitute a new surface-aware simulation.
"""
from pathlib import Path
import json,base64
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2];V=ROOT/'02_Visuals';D=ROOT/'03_Technical/Data';M=ROOT/'03_Technical/Models'

def host(uv):
    s=(uv[:,0]+.6)/1.2;t=uv[:,1]/1.8
    theta=(-140+280*s+38*t)*np.pi/180
    radius=1.5+.65*t*t+.20*np.sin(2*np.pi*s)*t
    height=2.6+.65*np.sin(np.pi*s)**2+.25*np.sin(2*np.pi*s)
    return np.column_stack((radius*np.sin(theta),radius*np.cos(theta),.12+t*height))

def perimeter():
    s=np.linspace(0,1,180,endpoint=False)
    return np.vstack((np.c_[-.6+1.2*s,s*0],np.c_[s*0+.6,1.8*s],np.c_[.6-1.2*s,s*0+1.8],np.c_[s*0-.6,1.8-1.8*s]))

def draw(ax,p,color='#99583f',lw=.55,closed=True):
    ax.plot(*(np.vstack((p,p[0])) if closed else p).T,color=color,lw=lw)
    ax.set_box_aspect((4.6,4.5,3.5));ax.set(xlim=(-2.4,2.4),ylim=(-2.4,2.4),zlim=(0,3.6));ax.set_axis_off();ax.view_init(22,-65)

def main():
    uv=np.load(D/'focused.npz')['uv'];patches=[np.c_[(uv[:,0]+.6)/4-.6+i*.3,uv[:,1]] for i in range(4)];curves=[host(v) for v in patches];p=np.concatenate(curves);edge=host(perimeter())
    def export_tube(points,radius,name):
        n=len(points);sides=12
        tang=np.roll(points,-1,axis=0)-np.roll(points,1,axis=0);tang/=np.linalg.norm(tang,axis=1)[:,None]
        guide=np.tile([0.,1.,0.],(n,1));guide[abs(tang[:,1])>.95]=[1,0,0]
        normal=np.cross(tang,guide);normal/=np.linalg.norm(normal,axis=1)[:,None];bi=np.cross(tang,normal)
        th=np.arange(sides)*2*np.pi/sides
        verts=(points[:,None,:]+radius*(normal[:,None,:]*np.cos(th)[None,:,None]+bi[:,None,:]*np.sin(th)[None,:,None])).reshape(-1,3)
        faces=[]
        for i in range(n):
            for j in range(sides):
                a=i*sides+j;b=i*sides+(j+1)%sides;c=((i+1)%n)*sides+(j+1)%sides;d=((i+1)%n)*sides+j
                faces.extend([[a,b,c],[a,c,d]])
        faces=np.array(faces);edges=np.sort(np.concatenate((faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]])),axis=1)
        assert np.all(np.unique(edges,axis=0,return_counts=True)[1]==2)
        with (M/f'{name}.obj').open('w') as f:
            f.write('# STRIA conceptual geometry. Units: metres.\n')
            for v in verts:f.write('v %.8f %.8f %.8f\n'%tuple(v))
            for face in faces+1:f.write('f %d %d %d\n'%tuple(face))
    for i,curve in enumerate(curves):export_tube(curve,.008,f'crescent_strand_{i}')
    export_tube(edge,.023,'crescent_frame')
    import trimesh,rhino3dm as rh
    from analyze_export import to_rhino
    doc=rh.File3dm();doc.Settings.ModelUnitSystem=rh.UnitSystem.Meters
    for name in [f'crescent_strand_{i}' for i in range(4)]+['crescent_frame']:
        mesh=trimesh.load(M/f'{name}.obj',process=False);(M/f'{name}.ply').write_bytes(mesh.export(file_type='ply'))
        layer=rh.Layer();layer.Name=name;idx=doc.Layers.Add(layer);a=rh.ObjectAttributes();a.LayerIndex=idx;doc.Objects.AddMesh(to_rhino(mesh),a)
    (M/'STRIA_Crescent.3dm').write_bytes(base64.b64decode(doc.Encode()))
    check=rh.File3dm.Read(str(M/'STRIA_Crescent.3dm'));assert len(check.Objects)==5 and all(o.Geometry.IsValid for o in check.Objects)
    np.savez_compressed(D/'crescent.npz',uv=uv,xyz=np.array(curves),perimeter=edge)
    old=np.linalg.norm(np.roll(uv,-1,axis=0)-uv,axis=1);seg=np.concatenate([np.linalg.norm(np.roll(c,-1,axis=0)-c,axis=1) for c in curves]);old=np.tile(old,4)
    report={'name':'Torqued crescent','mapping':'280 degree crescent; 38 degree height twist; flared radial loft','nodes':len(p),'closed_growth_loops':4,'path_length_m':float(seg.sum()),'bounds_centerline_m':np.ptp(p,axis=0).tolist(),'strand_diameter_m':.016,'frame_diameter_m':.046,'segment_stretch_min':float(min(seg/old)),'segment_stretch_max':float(max(seg/old)),'mesh_edge_incidence_two':True,'limits':'Non-isometric remapping of focused benchmark. Openness, clearance and bend statistics from cylinder do not transfer. No structural, joint or full swept-mesh intersection certification.'}
    (D/'showcase_metrics.json').write_text(json.dumps(report,indent=2))
    plt.rcParams.update({'font.family':'DejaVu Sans','savefig.facecolor':'#f6f3ec'})
    fig=plt.figure(figsize=(12,10),facecolor='#f6f3ec');ax=fig.add_axes([0,0,1,1],projection='3d');ax.set_facecolor('#f6f3ec');[draw(ax,c,lw=.65) for c in curves];draw(ax,edge,'#25373a',1.8)
    fig.savefig(V/'crescent_geometry.png',dpi=220);plt.close(fig)
    fig=plt.figure(figsize=(16,7),facecolor='#f6f3ec')
    for i in range(3):
        ax=fig.add_subplot(1,3,i+1,projection='3d');ax.set_facecolor('#f6f3ec')
        if i==0:
            for s in np.linspace(-.6,.6,15):draw(ax,host(np.c_[np.full(80,s),np.linspace(0,1.8,80)]),'#a4aaa0',.5,closed=False)
            for t in np.linspace(0,1.8,13):draw(ax,host(np.c_[np.linspace(-.6,.6,100),np.full(100,t)]),'#a4aaa0',.5,closed=False)
        if i>0:
            for c in curves:draw(ax,c,'#aa5e40',.4)
        draw(ax,edge,'#25373a',1)
        if i==2:ax.view_init(85,-90)
        ax.set_title(['01   HOST / FLARE + TWIST','02   FOUR MAPPED GROWTH LOOPS','03   OPEN CRESCENT / PLAN'][i],fontsize=11,color='#25373a',y=.91)
    fig.subplots_adjust(0,0,1,1,wspace=0);fig.savefig(V/'crescent_atlas.png',dpi=200);fig.savefig(V/'crescent_atlas.svg');plt.close(fig)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
