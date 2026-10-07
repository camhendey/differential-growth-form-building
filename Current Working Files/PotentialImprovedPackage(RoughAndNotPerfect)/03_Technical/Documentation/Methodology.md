# Methodology and verification contract

## 1. Evidence base

The supplied archive contains a Grasshopper definition, a four-page research paper and a 22-slide presentation dated December 2024. The definition's internal name is `Proj3_Final.gh`, despite its external Project2 filename. Its archive contains 65 objects including groups and controls, not 65 solver components. Saved library metadata records Grasshopper 8.11 and Kangaroo 2.5.3.

The native workflow maps a segmented seed to a lofted host surface and sends surface, length, collider and angle goals to BouncySolver. A downstream NURBS curve uses solver vertices. The archived piping branch was disconnected and disabled. The supplied mesh separately establishes that a thickened output was produced.

The additional 3DM contains one valid closed mesh: 416,521 vertices and 414,210 faces. Its bounding dimensions are approximately 197.628 x 167.301 x 227.136 unspecified model units. Exact coincident-vertex merging yields one connected component; every resulting edge has two incident faces. This test does not establish solid volume validity or absence of geometric self-intersection. Original source files are unchanged.

## 2. Independent solver

This is an implemented extension of the project's growth principles, not a byte-level or numerical recreation of Kangaroo. It deliberately uses a developable cylindrical surface so growth can be solved in intrinsic coordinates without an approximate nearest-surface projection at every step.

Domain: u in [-0.6, 0.6] m, v in [0, 1.8] m. Nodes are clamped to a 19 mm inset. Initial loop: 180 angular samples of a perturbed ellipse with nominal radii 0.20 and 0.40 m, centered at (0, 0.90 m). Its radius modulation is 1 + 0.035 sin(3t) + 0.025 cos(7t). A seeded Gaussian perturbation with standard deviation 0.15 mm breaks exact symmetry.

The displacement update combines:

- Elastic neighbor force: coefficient 0.45, rest length 27 mm.
- Laplacian term: coefficient 0.16, based on the previous and next node.
- Pair repulsion: coefficient 0.24, proportional to the shortfall below the pair's averaged local spacing target. Cyclic index neighbors within two indices are excluded.
- Displacement cap: 2 mm per iteration.

A KD-tree proposes pairs within the maximum 56 mm exclusion distance. This is a soft node-pair repulsion model, not continuous collision detection between moving segments. It can generate invalid geometry; downstream tests are therefore essential.

Every 40 iterations, segments longer than 17 mm can be split. The longest candidates are inserted in batches limited to approximately one twelfth of the current node count, without exceeding 3,500 nodes. Growth stops after 6,500 iterations. No equilibrium or convergence criterion is claimed.

### Spacing fields

The local exclusion target is `d(u,v) = 0.030 + 0.026 f(u,v)` metres.

- Uniform: f = 0.
- Height gradient: f = clip(v / 1.8, 0, 1).
- Focused: f = exp[-0.5 ((u / 0.30)^2 + ((v - 1.16) / 0.28)^2)].

The field is a control input, not an output guarantee. The final distribution also depends on seed, topology, domain, elastic forces and fairing.

### Fairing

Raw growth produces short-scale buckling. The output undergoes 30 Laplacian fairing steps at coefficient 0.25, then equal-arclength resampling to the same node count, then periodic Gaussian filtering with sigma 1 sample. This materially changes the geometry and can shorten the path. Every reported metric and export is computed after fairing. The animation includes the distinct final fairing step rather than concealing it.

## 3. Mapping and model geometry

For cylinder radius R = 1.45 m:

```
x = R sin(u/R)
y = R [1 - cos(u/R)]
z = v
```

The parameter derivatives have unit lengths and zero dot product; the intrinsic metric is Euclidean. Intrinsic arclength is therefore preserved by the continuous mapping. Finite exported chord lengths slightly under-approximate the corresponding continuous surface arcs. Arbitrary doubly curved surfaces do not share this guarantee.

The centerline is a cyclic polyline. A 12-sided circular cross-section of radius 4.5 mm is swept around it. The frame uses a 12 mm radius. Six concept ties use a 3 mm radius and connect designated frame positions to nearby strand vertices. Proposed feet are separate box meshes. These are geometric assembly elements, not verified mechanical connections or manufacturing tolerances.

## 4. Measurement definitions

### Openness

A front orthographic projection uses x and z. A 1 mm raster covers the nominal projected panel envelope. The projected centerline is stroked at 9 mm width with connected joints. Openness is one minus the fraction of occupied raster pixels.

The viewing zone is a 0.50 x 0.50 m square centered at x = 0, z = 1.16 m. The frame, ties, feet and scene are excluded. This is a reproducible projected centerline-stroke proxy, not a photometric simulation, exact swept-mesh silhouette or perceived privacy metric. Raster discretization and stroke geometry introduce approximation.

### Nonlocal spacing

Pairs of 3D centerline segments are proposed using a KD-tree over segment midpoints with a conservative search radius. Exact finite segment-to-segment distances are then calculated, considering interior and endpoint cases. Pairs with midpoint separation of 50 mm or less measured along the cyclic path are excluded as local neighbors. Reported minima apply to the remaining pairs. A conflict is counted when distance is below the nominal 9 mm strand diameter.

Zero flags in this test do not imply global swept-mesh self-intersection freedom. The local exclusion deliberately requires a separate curvature check, and neither test constitutes a complete mesh-intersection proof.

### Curvature

For turning angle theta between neighboring segment tangents and mean neighboring segment length l, discrete curvature is `2 sin(theta/2) / l`. Its reciprocal is the sampled bend radius. Vertices below the 4.5 mm strand radius are flagged. This is a numerical geometric screen, not a material-specific bend limit. A small positive margin is not manufacturing clearance.

### Surface deviation and topology

Deviation is measured at mapped centerline vertices using the cylinder equation. Floating-point-scale deviations are expected because the vertices are generated analytically. This says nothing about the suitability of the chosen surface for the application. Strand meshes are checked for watertight edge topology. Mesh triangle self-intersection is not exhaustively tested.

## 5. Experiment design

All three named studies use seed 17, 6,500 growth iterations, a 3,500-node cap, identical boundaries and identical post-processing. Local spacing field is the independent variable. Outputs are stored in NPZ files with saved states, allowing audit of both raw growth and final fairing.

The selected focused study was replayed with the final implementation. Coordinates were identical in the tested environment. A further seed-29 study produced 86.8% zone openness, a 30.05 m path and no flagged nonlocal spacing or sampled bend conflicts. This single perturbation is informative but does not establish broad robustness.

Recorded runtimes are diagnostic observations only. Concurrent rendering changed available CPU resources, so the recorded times must not be treated as a controlled performance benchmark.

## 6. Grasshopper repair

The audited binary tree is re-serialized and compared to the exact decompressed source before editing. The repaired copy:

1. Connects the final curve output to the Pipe curve input.
2. Enables the Pipe and subsequent display branch.
3. Sets the final NURBS component's periodic input true.
4. Saves under a distinct filename.

Native execution is not available in this environment. Periodicity requests closure but does not prove correct point ordering. The repaired file must be run and inspected in Rhino/Kangaroo before being accepted as a reproduction. It does not contain the new Python field solver.

## 7. Claim boundaries

No measured material saving, fabrication time, cost, structural behavior, acoustic performance, daylight benefit or human outcome is claimed. The object is a digital design proposal, not a production-ready product. The three-panel scene is a visualization of potential use, not site evidence.
