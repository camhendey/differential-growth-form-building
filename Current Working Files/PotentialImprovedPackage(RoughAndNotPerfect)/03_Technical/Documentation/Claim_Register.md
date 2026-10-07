# Claim register

| Claim | Evidence | Boundary |
|---|---|---|
| Original Grasshopper implementation independently developed by Cameron Hendey | User's explicit authorship statement in this conversation | Informed by prior differential-growth examples; no claim to invention of differential growth |
| Native workflow uses surface, length, collider and bending goals | `Data/Original_Definition_Decoded.json`, objects 6, 7, 14, 18, 21 | Serialized graph audit, not native execution |
| Growth occurred on a prescribed 3D form | Supplied recording and accompanying four-view screenshots | Visual behavior, not quantified physical testing |
| A thickened final source mesh exists | `05_Source_Evidence/DifferentialGrowthModelOutput.3dm` | Physical dimensions unspecified; no fabrication evidence |
| New solver implements local spacing fields and refinement | `Code/growth.py`; saved NPZ records | Independent Python model, not numerically equivalent to Kangaroo |
| Selected zone openness is 87.7% | `Data/metrics.json`, focused.view_zone_open_fraction | Defined 1 mm front-projection stroke proxy, frame excluded |
| Improvement relative to uniform is 10.3 percentage points | (0.877048 - 0.773584) x 100 | Not 10.3% relative improvement; not a measured user outcome |
| Selected length is 28.20 m | `metrics.json`, focused.path_length_m | Proposed design scale; not measured material usage |
| Focused uses 12.4% less path than gradient | 1 - 28.19700220223188 / 32.19353888481813 | Geometric trade-off only, not manufacturing or cost saving |
| No selected nonlocal clearance flags | `metrics.json`, focused.clearance_violating_segment_pairs | 50 mm path-neighbor exclusion; not complete swept-mesh self-intersection proof |
| Uniform study has ten tight-bend flags | `metrics.json`, uniform.bend_radius_below_strand_radius_vertices | Ten sampled vertices, not necessarily ten distinct physical defects |
| Seven tests pass | `validation.json`, test_log | Limited tests of implemented functions, not comprehensive software certification |
| Full selected run repeats exactly | `validation.json`, full_replay | Exact in tested environment; cross-platform numerical identity not established |
| Alternate seed passes implemented selected-geometry checks | `validation.json`, seed_sensitivity | One alternate seed, no statistical robustness claim |
| Grasshopper repair preserves binary source before editing | Assertion in `repair_definition.py` executed successfully | Edited definition remains native-runtime unverified |
| Rendered screen assembly exists digitally | Native Rhino models, mesh exports, `render.py` | Material, joints, supports and stability are proposed, not engineered |
| All project renders derive from geometry | `render.py` loads source-normalized or generated PLY meshes | Gallery, finishes and scale are design visualization choices |

No structural, acoustic, daylight, manufacturing-efficiency, business-impact or physical-fabrication claim is authorized by this evidence.

## Crescent visual revision

Geometry, mapping and 198.45 m centerline claim: showcase.py, crescent.npz and showcase_metrics.json. Four separately closed loops, not one global closed path. Mesh edge incidence checked; native file reopened with five valid objects. No physical or global self-intersection validation. Collages are interpretive, not measurement evidence. See Visual_Revision.md.
