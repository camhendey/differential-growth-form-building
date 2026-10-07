"""Repair the archived output wiring without pretending a native run occurred.

Re-serializes the audited GH binary tree. A round-trip assertion precedes edits.
Only reconnects final curve to Pipe, enables display branch, and closes output.
Rhino/Kangaroo execution is still required to validate solver point ordering.
"""
import json, struct, uuid, zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def pack(fmt,*v):return struct.pack('<'+fmt,*v)
def s(v):
    b=v.encode();n=len(b);a=bytearray()
    while n>=128:a.append((n&127)|128);n>>=7
    a.append(n);return bytes(a)+b
def value(t,v):
    formats={1:'?',2:'B',3:'i',4:'q',5:'f',6:'d',7:'4I',8:'q',30:'2i',31:'2f',32:'2i',33:'2f',34:'4i',35:'4f',36:'I',50:'2d',51:'3d',52:'4d',60:'2d',61:'4d',70:'6d',71:'6d',72:'9d',80:'3i'}
    if t in formats:return pack(formats[t],*(v if isinstance(v,list) else [v]))
    if t==9:return uuid.UUID(v).bytes_le
    if t==10:return s(v)
    if t in (20,37):return pack('i',v['bytes'])+bytes.fromhex(v['hex'])
    if t==21:return pack('i',len(v))+pack(str(len(v))+'d',*v)
    raise ValueError(t)
def encode(c):
    b=s(c['name'])+pack('iii',c['index'],len(c['items']),len(c['chunks']))
    for i in c['items']:b+=s(i['name'])+pack('ii',i['index'],i['type'])+value(i['type'],i['value'])
    return b+b''.join(encode(x) for x in c['chunks'])
def walk(c):
    yield c
    for x in c['chunks']:yield from walk(x)
def values(c):return {i['name']:i['value'] for i in c['items']}

def main():
    import zipfile
    tree=json.loads((ROOT/'03_Technical/Data/Original_Definition_Decoded.json').read_text())
    with zipfile.ZipFile(ROOT/'05_Source_Evidence/ARC3201_CameronHendey_Project3.zip') as z:
        raw=z.read(next(n for n in z.namelist() if n.endswith('.gh')))
    assert encode(tree)==zlib.decompress(raw,-15),'Round trip must preserve source'
    objects={c['index']:c for c in walk(tree) if c['name']=='Object'}
    final_container=objects[17]['chunks'][0]
    final_output=next(c for c in final_container['chunks'] if c['name']=='param_output')
    output_id=values(final_output)['InstanceGuid']
    pipe=objects[57]['chunks'][0]
    curve_in=next(c for c in pipe['chunks'] if c['name']=='param_input' and c['index']==0)
    for i in curve_in['items']:
        if i['name']=='SourceCount':i['value']=1
    curve_in['items'].append({'name':'Source','index':0,'type':9,'value':output_id})
    for idx in range(57,62):
        for c in walk(objects[idx]):
            for i in c['items']:
                if i['name']=='Locked':i['value']=False
    periodic=next(c for c in final_container['chunks'] if c['name']=='param_input' and c['index']==2)
    for c in walk(periodic):
        for i in c['items']:
            if i['name']=='boolean':i['value']=True
    for c in walk(tree):
        if c['name']=='DefinitionProperties':
            for i in c['items']:
                if i['name']=='Name':i['value']='STRIA_Baseline_Output_Repair.gh'
    compressor=zlib.compressobj(wbits=-15)
    out=ROOT/'03_Technical/Models/STRIA_Baseline_Output_Repair.gh'
    out.write_bytes(compressor.compress(encode(tree))+compressor.flush())
    print('Binary round-trip passed; repair saved. Native execution NOT performed.')

if __name__=='__main__':main()
