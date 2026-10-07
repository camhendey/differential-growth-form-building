"""Measured geometry figures and growth animation, derived from saved runs."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image,ImageDraw,ImageFont
from growth import surface,field,WIDTH,HEIGHT
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'03_Technical/Data';OUT=ROOT/'02_Visuals'
CORAL='#CA654A';NAVY='#13242C';BLUE='#54796C';PAPER='#F6F3EC'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':NAVY,'axes.labelcolor':NAVY,'font.size':11,'svg.fonttype':'none'})

def finish(fig,name):
    fig.savefig(OUT/f'{name}.svg',facecolor=fig.get_facecolor(),bbox_inches='tight');fig.savefig(OUT/f'{name}.png',dpi=220,facecolor=fig.get_facecolor(),bbox_inches='tight');plt.close(fig)

def main():
    fig,axs=plt.subplots(1,3,figsize=(12,6),facecolor=PAPER)
    for ax,name in zip(axs,['uniform','gradient','focused']):
        p=np.load(DATA/f'{name}.npz')['uv'];xyz=surface(p);xz=xyz[:,[0,2]];xz=np.vstack((xz,xz[0]));ax.plot(*xz.T,c=CORAL,lw=1.5)
        ax.add_patch(Rectangle((-.25,.91),.5,.5,fill=False,edgecolor=BLUE,lw=1,ls='--'))
        ax.add_patch(Rectangle((-.583,0),1.166,1.8,fill=False,edgecolor=NAVY,lw=.8))
        ax.set(xlim=(-.65,.65),ylim=(-.05,1.9),aspect='equal');ax.axis('off');ax.set_title(name.upper(),fontsize=13,fontweight='bold')
    finish(fig,'comparison')
    fig,axs=plt.subplots(1,3,figsize=(12,5.5),facecolor=PAPER)
    u,v=np.meshgrid(np.linspace(-.6,.6,140),np.linspace(0,1.8,210));uv=np.column_stack((u.ravel(),v.ravel()))
    for ax,name in zip(axs,['uniform','gradient','focused']):
        f=field(uv,name).reshape(u.shape)
        from matplotlib.colors import LinearSegmentedColormap
        cmap=LinearSegmentedColormap.from_list('spacing',['#eae4d7','#a7b7a6','#476b5e'])
        ax.imshow(f,extent=[-.6,.6,0,1.8],origin='lower',cmap=cmap,vmin=0,vmax=1)
        if name!='uniform':ax.contour(u,v,f,levels=[.2,.4,.6,.8],colors='#f6f3ec',linewidths=.6)
        curve=np.load(DATA/f'{name}.npz')['uv'];ax.plot(*np.vstack((curve,curve[0])).T,c='#24382e',lw=.45,alpha=.7)
        ax.text(0,-.14,'30 mm' if name=='uniform' else '30 → 56 mm',ha='center',fontsize=11,color=NAVY)
        ax.set_title(name.upper(),fontweight='bold');ax.axis('off')
    finish(fig,'fields')
    data=np.load(DATA/'focused.npz');ks=['frame_00000','frame_00600','frame_01200','frame_02400','frame_04200','frame_06531']
    fig,axs=plt.subplots(1,6,figsize=(16,4.6),facecolor=PAPER)
    for ax,k in zip(axs,ks):
        p=data[k];q=np.vstack((p,p[0]));ax.plot(*q.T,c=CORAL,lw=.8);ax.set(xlim=(-.62,.62),ylim=(0,1.8),aspect='equal');ax.axis('off');ax.set_title('FAIRED' if k.endswith('6531') else str(int(k[-5:])),fontsize=11)
    finish(fig,'growth_sequence')
    # One deliberately sparse technical front elevation with design dimensions.
    fig,ax=plt.subplots(figsize=(6.5,8),facecolor=PAPER)
    p=surface(data['uv']);ax.plot(p[:,0],p[:,2],c=CORAL,lw=1)
    ax.add_patch(Rectangle((-.583,0),1.166,1.8,fill=False,ec=NAVY,lw=2))
    ax.annotate('',(-.72,0),(-.72,1.8),arrowprops={'arrowstyle':'<->','color':NAVY});ax.text(-.77,.90,'1.80 m',rotation=90,ha='center',va='center')
    ax.annotate('',(-.583,-.12),(.583,-.12),arrowprops={'arrowstyle':'<->','color':NAVY});ax.text(0,-.20,'1.17 m projected width',ha='center')
    ax.text(0,-.31,'1.20 m unrolled width / R 1.45 m',ha='center',fontsize=10)
    ax.set(xlim=(-.95,.85),ylim=(-.38,1.88),aspect='equal');ax.axis('off');finish(fig,'elevation')
    frames=[];font=ImageFont.truetype(str(OUT/'Fonts/DejaVuSans.ttf'),22)
    for k in sorted(x for x in data.files if x.startswith('frame_')):
        im=Image.new('RGB',(720,1000),PAPER);d=ImageDraw.Draw(im);p=surface(data[k]);coords=[(360+x*480,930-z*480) for x,y,z in p]
        d.rectangle([80,66,640,932],outline=NAVY,width=2);d.line(coords+[coords[0]],fill=CORAL,width=3,joint='curve')
        label='Final geometry / fairing applied' if k.endswith('6531') else f'Iteration {int(k[-5:]):,}'
        d.text((35,18),'STRIA   /   '+label,font=font,fill=NAVY);frames.append(im)
    frames[0].save(OUT/'Growth_Sequence.gif',save_all=True,append_images=frames[1:],duration=100,loop=0)
    print('Geometry figures complete',flush=True)

if __name__=='__main__':main()
