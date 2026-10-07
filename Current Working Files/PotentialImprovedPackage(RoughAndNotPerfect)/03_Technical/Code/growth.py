"""STRIA: differential growth on an isometrically unrolled cylindrical screen.

Independent Python development, not a numerical reproduction of Kangaroo.
All design dimensions are metres. Original source geometry remains unitless.
Run: python growth.py --out ../Data --steps 6500
"""
from __future__ import annotations
import argparse
import json
import time
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scipy.ndimage import gaussian_filter1d

WIDTH, HEIGHT, RADIUS = 1.2, 1.8, 1.45
STRAND_RADIUS = 0.0045

def surface(uv):
    """Cylinder whose unrolled coordinates preserve intrinsic lengths."""
    u, v = np.asarray(uv).T
    theta = u / RADIUS
    return np.column_stack((RADIUS * np.sin(theta), RADIUS * (1 - np.cos(theta)), v))

def field(uv, mode):
    u, v = np.asarray(uv).T
    if mode == 'uniform': return np.zeros(len(u))
    if mode == 'gradient': return np.clip(v / HEIGHT, 0, 1)
    return np.exp(-0.5 * ((u / 0.30)**2 + ((v - 1.16) / 0.28)**2))

def spacing(uv, mode):
    return 0.030 + 0.026 * field(uv, mode)

def simulate(mode='focused', seed=17, steps=6500, save_every=100):
    rng = np.random.default_rng(seed)
    t = np.linspace(0, 2*np.pi, 180, endpoint=False)
    rad = 1 + 0.035*np.sin(3*t) + 0.025*np.cos(7*t)
    p = np.column_stack((0.20*rad*np.cos(t), 0.9 + 0.40*rad*np.sin(t)))
    p += rng.normal(0, 0.00015, p.shape)
    snapshots = []
    start = time.perf_counter()
    for iteration in range(steps + 1):
        if iteration % save_every == 0 or iteration == steps:
            snapshots.append((iteration, p.copy()))
        if iteration == steps: break
        n = len(p)
        nxt = np.roll(p, -1, axis=0)
        delta = nxt-p
        lengths = np.linalg.norm(delta, axis=1)
        edge_force = 0.45 * (lengths-0.027)[:, None] * delta / np.maximum(lengths[:, None], 1e-12)
        force = edge_force - np.roll(edge_force, 1, axis=0)
        force += 0.16 * (np.roll(p, 1, axis=0) + nxt - 2*p)
        local = spacing(p, mode)
        pairs = cKDTree(p).query_pairs(0.056, output_type='ndarray')
        if len(pairs):
            a,b = pairs.T
            idxdist=np.minimum(abs(a-b),n-abs(a-b))
            d=p[a]-p[b];dist=np.linalg.norm(d,axis=1)
            target=(local[a]+local[b])*0.5
            mask=(idxdist>2)&(dist<target)&(dist>1e-12)
            a,b,d,dist,target=a[mask],b[mask],d[mask],dist[mask],target[mask]
            rep=0.24*(target-dist)[:,None]*d/dist[:,None]
            np.add.at(force,a,rep);np.add.at(force,b,-rep)
        movement=np.linalg.norm(force,axis=1)
        force *= np.minimum(1,0.002/np.maximum(movement,1e-12))[:,None]
        p += force
        p[:,0]=np.clip(p[:,0],-WIDTH/2+0.019,WIDTH/2-0.019)
        p[:,1]=np.clip(p[:,1],0.019,HEIGHT-0.019)
        if iteration % 40 == 0 and len(p)<3500:
            q=np.roll(p,-1,axis=0);split=np.linalg.norm(q-p,axis=1)>0.017
            if np.any(split):
                candidates=np.flatnonzero(split)
                budget=min(3500-len(p),max(1,len(p)//12))
                choose=candidates[np.argsort(np.linalg.norm(q-p,axis=1)[candidates])[-budget:]]
                split[:]=False;split[choose]=True
                count=1+split.astype(int);ids=np.cumsum(count)-count
                new=np.empty((count.sum(),2));new[ids]=p
                new[ids[split]+1]=(p[split]+q[split])*0.5;p=new
    # Explicit post-relaxation smooths sub-resolution buckling. All validation
    # is performed on this final, changed geometry, never on the raw curve.
    for _ in range(30):
        p += 0.25*(np.roll(p,1,axis=0)+np.roll(p,-1,axis=0)-2*p)
    # Fair on equal arc-length samples: index-space smoothing alone can leave
    # sharp tips where adaptive samples cluster. Final measurements follow this.
    q=np.vstack((p,p[0]));arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(q,axis=0),axis=1))]
    samples=np.linspace(0,arc[-1],len(p),endpoint=False)
    p=np.column_stack([np.interp(samples,arc,q[:,i]) for i in range(2)])
    p=gaussian_filter1d(p,1,axis=0,mode='wrap')
    snapshots.append((steps+31,p.copy()))
    return p,snapshots,time.perf_counter()-start

def run(out,steps=6500):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    manifest={'dimensions_m':{'width':WIDTH,'height':HEIGHT,'cylinder_radius':RADIUS,'strand_radius':STRAND_RADIUS},'solver':'Independent intrinsic-coordinate solver; not Kangaroo-equivalent','runs':[]}
    for mode in ('uniform','gradient','focused'):
        p,snaps,elapsed=simulate(mode,17,steps)
        np.savez_compressed(out/f'{mode}.npz',uv=p,xyz=surface(p),**{f'frame_{i:05d}':a for i,a in snaps})
        entry={'mode':mode,'seed':17,'steps':steps,'nodes':len(p),'runtime_seconds':elapsed}
        manifest['runs'].append(entry);print(entry,flush=True)
    (out/'run_manifest.json').write_text(json.dumps(manifest,indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='../Data');ap.add_argument('--steps',type=int,default=6500)
    args=ap.parse_args();run(args.out,args.steps)
