"""Validate deliverables, create portable image copies, index and package."""
from pathlib import Path
import hashlib,json,zipfile
import numpy as np
import rhino3dm as rh
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def main():
    for name in ['hero','studio','original','detail','Showcase_Courtyard','Showcase_Interior','crescent_render']:
        im=Image.open(ROOT/f'02_Visuals/{name}.png').convert('RGB');im.thumbnail((1600,1600));im.save(ROOT/f'04_Web/{name}.jpg',quality=90,optimize=True)
    checks={}
    for name in ['uniform','gradient','focused','Crescent']:
        doc=rh.File3dm.Read(str(ROOT/f'03_Technical/Models/STRIA_{name}.3dm'))
        checks[name]={'objects':len(doc.Objects),'units':str(doc.Settings.ModelUnitSystem),'all_geometry_valid':all(o.Geometry.IsValid for o in doc.Objects),'layers':[l.Name for l in doc.Layers]}
    checks['pdf_present']=(ROOT/'01_Portfolio/STRIA_Master_Case_Study.pdf').is_file()
    checks['full_replay_exact']=json.loads((ROOT/'03_Technical/Data/validation.json').read_text())['full_replay']['array_equal']
    assert all(checks[n]['all_geometry_valid'] for n in ['uniform','gradient','focused'])
    assert checks['full_replay_exact']
    (ROOT/'03_Technical/Data/delivery_checks.json').write_text(json.dumps(checks,indent=2))
    index=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.name!='Package_Index.json':
            index.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    (ROOT/'Package_Index.json').write_text(json.dumps(index,indent=2))
    dest=ROOT.parent/'STRIA_Complete_Project.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(ROOT.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,'STRIA/'+str(p.relative_to(ROOT)))
    with zipfile.ZipFile(dest) as z:assert z.testzip() is None
    print(json.dumps({'package':str(dest),'bytes':dest.stat().st_size,'indexed_files':len(index),'checks':checks},indent=2))

if __name__=='__main__':main()
