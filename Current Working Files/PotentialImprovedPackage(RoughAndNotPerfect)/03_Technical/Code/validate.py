"""Run tests, repeat the selected full simulation, and record seed sensitivity."""
import json,unittest,io,time,platform
from pathlib import Path
import numpy as np
from growth import simulate,surface,STRAND_RADIUS
from analyze_export import metrics
import tests
ROOT=Path(__file__).resolve().parents[2];DATA=ROOT/'03_Technical/Data'
stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(tests))
reference=np.load(DATA/'focused.npz')['uv']
p,_,elapsed=simulate('focused',17,6500)
delta=float(np.max(abs(reference-p)))
print('Full replay maximum coordinate difference',delta,flush=True)
alt,snap,alt_time=simulate('focused',29,6500)
np.savez_compressed(DATA/'focused_seed29.npz',uv=alt,xyz=surface(alt))
record={'unit_tests_passed':result.wasSuccessful(),'unit_tests_run':result.testsRun,'test_log':stream.getvalue(),'full_replay':{'seed':17,'steps':6500,'runtime_seconds':elapsed,'maximum_coordinate_difference_m':delta,'array_equal':bool(np.array_equal(p,reference))},'seed_sensitivity':{'seed':29,'steps':6500,'runtime_seconds':alt_time,'metrics':metrics(alt)},'environment':{'python':platform.python_version(),'platform':platform.platform()},'not_verified':['Kangaroo numerical equivalence','Native execution of repaired Grasshopper definition','Material and structural performance','Nozzle access and deposition sequence','Full swept-mesh self-intersection analysis','Frame and tie mechanical connections']}
(DATA/'validation.json').write_text(json.dumps(record,indent=2))
manifest=json.loads((DATA/'run_manifest.json').read_text());manifest['dimensions_m']['strand_radius']=STRAND_RADIUS;manifest['postprocessing']='30 index-space fairing steps, uniform arclength resampling, Gaussian sigma 1 sample; all metrics measured afterward';manifest['design_scale']='Proposed scale for new screen only; original file units unknown'
(DATA/'run_manifest.json').write_text(json.dumps(manifest,indent=2))
print('Validation saved',flush=True)
