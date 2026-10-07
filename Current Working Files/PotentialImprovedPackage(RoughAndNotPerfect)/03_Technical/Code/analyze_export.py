"""Geometry validation and native/model exports. No fabrication certification."""
from pathlib import Path
import json
import base64
import numpy as np
from PIL import Image,ImageDraw
from scipy.spatial import cKDTree
from shapely.geometry import LineString
import trimesh
import rhino3dm as rh
from growth import WIDTH,HEIGHT,RADIUS,STRAND_RADIUS,surface

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'03_Technical/Data';MODELS=ROOT/'03_Technical/Models'

def segment_distances(a,b,c,d):
    """Vectorized finite 3D segment distances, including endpoint cases."""
    u=b-a;v=d-c;w=a-c
    aa=(u*u).sum(1);bb=(u*v).sum(1);cc=(v*v).sum(1)
    dd=(u*w).sum(1);ee=(v*w).sum(1);den=aa*cc-bb*bb
    ss=np.divide(bb*ee-cc*dd,den,out=np.zeros_like(den),where=abs(den)>1e-20)
    tt=np.divide(aa*ee-bb*dd,den,out=np.zeros_like(den),where=abs(den)>1e-20)
    out=np.where((ss>=0)&(ss<=1)&(tt>=0)&(tt<=1)&(abs(den)>1e-20),np.linalg.norm(w+ss[:,None]*u-tt[:,None]*v,axis=1),np.inf)
    for p,x,e,el in [(a,c,v,cc),(b,c,v,cc),(c,a,u,aa),(d,a,u,aa)]:
        t=np.clip(((p-x)*e).sum(1)/np.maximum(el,1e-20),0,1)
        out=np.minimum(out,np.linalg.norm(p-x-t[:,None]*e,axis=1))
    return out

def tube(points,radius,closed=True,sides=12):
    p=np.asarray(points);n=len(p)
    tang=np.roll(p,-1,axis=0)-np.roll(p,1,axis=0)
    if not closed:tang[0]=p[1]-p[0];tang[-1]=p[-1]-p[-2]
    tang/=np.linalg.norm(tang,axis=1)[:,None]
    guide=np.tile([0.,1.,0.],(n,1))
    guide[abs(tang[:,1])>.95]=[1,0,0]
    normal=np.cross(tang,guide);normal/=np.linalg.norm(normal,axis=1)[:,None]
    bi=np.cross(tang,normal)
    th=np.arange(sides)*2*np.pi/sides
    verts=(p[:,None,:]+radius*(normal[:,None,:]*np.cos(th)[None,:,None]+bi[:,None,:]*np.sin(th)[None,:,None])).reshape(-1,3)
    faces=[]
    for i in range(n if closed else n-1):
        ni=(i+1)%n
        for j in range(sides):
            a=i*sides+j;b=i*sides+(j+1)%sides;c=ni*sides+(j+1)%sides;d=ni*sides+j
            faces.extend([[a,b,c],[a,c,d]])
    if not closed:
        verts=np.vstack((verts,p[0],p[-1]));i0=n*sides;i1=i0+1
        for j in range(sides):faces.extend([[i0,(j+1)%sides,j],[i1,(n-1)*sides+j,(n-1)*sides+(j+1)%sides]])
    mesh=trimesh.Trimesh(verts,faces,process=False);mesh.fix_normals();return mesh

def metrics(uv):
    p=surface(uv);q=np.roll(p,-1,axis=0);seg=np.linalg.norm(q-p,axis=1)
    arc=np.r_[0,np.cumsum(seg)];mid=(p+q)/2
    pairs=cKDTree(mid).query_pairs(.075+seg.max(),output_type='ndarray')
    a,b=pairs.T;gap=abs((arc[a]+seg[a]/2)-(arc[b]+seg[b]/2));gap=np.minimum(gap,arc[-1]-gap)
    keep=gap>.050;a,b=a[keep],b[keep]
    distances=segment_distances(p[a],q[a],p[b],q[b])
    unit=(q-p)/seg[:,None];angle=np.arccos(np.clip((unit*np.roll(unit,1,axis=0)).sum(1),-1,1))
    curvature=2*np.sin(angle/2)/np.maximum((seg+np.roll(seg,1))/2,1e-12)
    # A 1 mm orthographic centerline-stroke mask, a geometric openness proxy.
    scale=1000;w=int(2*RADIUS*np.sin(WIDTH/(2*RADIUS))*scale);h=int(HEIGHT*scale)
    image=Image.new('L',(w,h),0);draw=ImageDraw.Draw(image)
    coords=[(float(x*scale+w/2),float((HEIGHT-z)*scale)) for x,y,z in p]
    draw.line(coords+[coords[0]],fill=255,width=round(STRAND_RADIUS*2*scale),joint='curve')
    mask=np.array(image)>0
    zone=mask[int((HEIGHT-1.41)*scale):int((HEIGHT-.91)*scale),w//2-250:w//2+250]
    deviation=abs(np.sqrt(p[:,0]**2+(p[:,1]-RADIUS)**2)-RADIUS)
    return {'nodes':len(p),'path_length_m':float(seg.sum()),'front_open_fraction':float(1-mask.mean()),'view_zone_open_fraction':float(1-zone.mean()),'minimum_nonlocal_centerline_distance_m':float(distances.min()),'clearance_violating_segment_pairs':int((distances<2*STRAND_RADIUS).sum()),'candidate_segment_pairs_checked':len(distances),'nonlocal_arc_exclusion_m':.050,'centerline_simple_unrolled':bool(LineString(np.vstack((uv,uv[0]))).is_simple),'max_surface_deviation_m':float(deviation.max()),'minimum_discrete_bend_radius_m':float(1/max(curvature)),'bend_radius_below_strand_radius_vertices':int((curvature>1/STRAND_RADIUS).sum()),'median_discrete_bend_radius_m':float(np.median(1/np.maximum(curvature,1e-12))),'closure':'cyclic indexed polyline','openness_method':'1 mm front-view stroke raster; 9 mm strand; frame excluded; 0.5 x 0.5 m central zone at z=1.16 m'}

def to_rhino(mesh):
    out=rh.Mesh()
    for v in mesh.vertices:out.Vertices.Add(*v)
    for f in mesh.faces:out.Faces.AddFace(*map(int,f))
    out.Normals.ComputeNormals();return out

def frame_points():
    t=np.linspace(-WIDTH/2,WIDTH/2,120)
    uv=np.vstack([np.column_stack((t,np.zeros_like(t))),
                  np.column_stack((np.full(100,WIDTH/2),np.linspace(0,HEIGHT,100))),
                  np.column_stack((t[::-1],np.full_like(t,HEIGHT))),
                  np.column_stack((np.full(100,-WIDTH/2),np.linspace(HEIGHT,0,100)))])
    return surface(uv[[i for i in range(440) if i not in [120,220,340,439]]])

def main():
    MODELS.mkdir(parents=True,exist_ok=True);results={}
    for name in ['uniform','gradient','focused']:
        uv=np.load(DATA/f'{name}.npz')['uv'];p=surface(uv);results[name]=metrics(uv)
        strand=tube(p,STRAND_RADIUS);frame=tube(frame_points(),.012)
        ties=[]
        for u in [-WIDTH/2,WIDTH/2]:
            for z in [.30,.90,1.50]:
                anchor=np.array([u,z]);idx=np.argmin(np.linalg.norm(uv-anchor,axis=1))
                ties.append(tube(surface(np.linspace(anchor,uv[idx],10)),.003,closed=False))
        ties=trimesh.util.concatenate(ties);(MODELS/f'{name}_ties.ply').write_bytes(ties.export(file_type='ply'))
        (MODELS/f'{name}_strand.ply').write_bytes(strand.export(file_type='ply'))
        (MODELS/f'{name}_strand.obj').write_text(strand.export(file_type='obj'))
        (MODELS/'frame.ply').write_bytes(frame.export(file_type='ply'))
        doc=rh.File3dm();doc.Settings.ModelUnitSystem=rh.UnitSystem.Meters
        feet=[]
        for x in [-.48,.48]:
            foot=trimesh.creation.box(extents=[.065,.48,.024]);foot.apply_translation([x,.06,.012]);feet.append(foot)
        feet=trimesh.util.concatenate(feet)
        for mesh,label in [(strand,'Growth strand'),(frame,'Concept frame'),(ties,'Concept mounting ties - unengineered'),(feet,'Concept feet - stability unverified')]:
            layer=rh.Layer();layer.Name=label;idx=doc.Layers.Add(layer);attrs=rh.ObjectAttributes();attrs.LayerIndex=idx;attrs.Name=label
            doc.Objects.AddMesh(to_rhino(mesh),attrs)
        pl=rh.PolylineCurve([rh.Point3d(*a) for a in np.vstack((p,p[0]))]);attr=rh.ObjectAttributes();attr.Name='Validated centerline';doc.Objects.AddCurve(pl,attr)
        payload=base64.b64decode(doc.Encode())
        assert rh.File3dm.FromByteArray(payload) is not None,'Native serialization failed'
        path=MODELS/f'STRIA_{name}.3dm';path.write_bytes(payload)
        check=rh.File3dm.Read(str(path));assert check is not None,'Native reopen failed'
        assert len(check.Objects)==5 and all(o.Geometry.IsValid for o in check.Objects)
        results[name]['strand_mesh_watertight']=bool(strand.is_watertight)
        print(name,results[name],flush=True)
    (DATA/'metrics.json').write_text(json.dumps(results,indent=2))
    original=rh.File3dm.Read(str(ROOT/'05_Source_Evidence/DifferentialGrowthModelOutput.3dm')).Objects[0].Geometry
    vv=np.array([[p.X,p.Y,p.Z] for p in original.Vertices]);ff=[]
    for f in original.Faces:
        a,b,c,d=f;ff.append([a,b,c])
        if c!=d:ff.append([a,c,d])
    vv-=vv.min(0);vv/=np.ptp(vv[:,2]);vv[:,:2]-=np.ptp(vv[:,:2],axis=0)/2
    (MODELS/'original_display_normalized.ply').write_bytes(trimesh.Trimesh(vv,ff,process=False).export(file_type='ply'))

if __name__=='__main__':main()
