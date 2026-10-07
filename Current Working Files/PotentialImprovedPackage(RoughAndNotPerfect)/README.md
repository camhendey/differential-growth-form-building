# STRIA

Controlled growth for porous space.

A digital design study by Cameron Hendey. The project connects surface-based differential-growth modelling with explicit controls, comparative studies and geometric verification. The main spatial proposal is a torqued crescent enclosure, supported by a controlled cylindrical-screen benchmark.

## Start here

- `01_Portfolio/STRIA_Master_Case_Study.pdf`: the 18-page illustrated project record.
- `03_Technical/Models/STRIA_focused.3dm`: selected Rhino model, in proposed design metres. Named layers separate the strand, frame, mounting ties and feet; the closed centerline is also included.
- `02_Visuals/Showcase_Courtyard.png` and `Showcase_Interior.png`: artistic architectural showcase collages.
- `03_Technical/Models/STRIA_Crescent.3dm`: new principal form with four growth loops and perimeter.
- `03_Technical/Documentation/Visual_Revision.md`: mapping, image provenance and revision details.
- `02_Visuals/Growth_Sequence.gif`: saved growth states followed by final fairing.
- `03_Technical/Documentation/Methodology.md`: numerical method, definitions and limits.
- `03_Technical/Data/metrics.json`: machine-readable geometric comparisons.
- `03_Technical/Data/validation.json`: test log, full-run replay and alternate-seed evidence.
- `05_Source_Evidence`: untouched original evidence and source archive.

## What is completed

1. Audited the original Grasshopper definition and recovered its complete binary data tree.
2. Preserved and inspected the supplied output mesh and growth recording.
3. Implemented an independent Python growth solver with three local spacing fields, adaptive refinement, fairing and an explicit cylindrical mapping.
4. Executed three matched studies and an additional seed-sensitivity run.
5. Reproduced the selected full run exactly in the tested environment.
6. Measured front-view openness, path length, nonlocal spacing and sampled curvature on final geometry.
7. Exported native Rhino models, meshes, source code, editable SVG graphics, renders and a project PDF.
8. Created a separately named repair of the archived Grasshopper output branch. This file is NOT native-runtime verified.

## Main findings from the cylindrical benchmark

The selected focused-field study has 87.7% geometric openness in the specified viewing zone, compared with 77.4% for uniform spacing. Its centerline is 28.20 m long at the proposed screen scale. The selected curve has no flagged nonlocal clearance conflicts in the implemented check and no sampled bend-radius flags at a 4.5 mm strand radius.

The uniform comparison retains ten tight-bend flags. It is retained as an informative baseline, not a fabrication-ready alternative. Results are geometric design evidence, not physical performance claims.

## Reproduce the studies

The delivered models, images and PDF can be opened without running any code. Code was tested on Linux with Python 3.12.14. Numerical identity on another platform or package version is not guaranteed.

From `03_Technical/Code`, install dependencies into a Python environment, then run:

```bash
python -m pip install -r requirements.txt
python growth.py --out ../Data --steps 6500
python analyze_export.py
python -m unittest tests -v
python validate.py
python figures.py
python render.py --kind hero --resolution 2400 --spp 160
python render.py --kind studio --resolution 2000 --spp 160
python render.py --kind detail --resolution 1800 --spp 160
python render.py --kind original --resolution 1800 --spp 160
python showcase.py
python render_crescent.py
python build_pdf.py
```

These commands intentionally replace generated outputs inside this package. Keep the delivered package as a baseline before experimenting. The original evidence folder is not rewritten. The optional `repair_definition.py` regenerates the separate native Grasshopper repair from the preserved source and decoded tree.

Rendering is CPU path tracing and can take materially longer than numerical analysis. The package does not require access to a Rhino licence for the independent Python study. Editing or running the Grasshopper definition requires Rhino/Grasshopper and Kangaroo.

## Boundaries

- The screen's 1.80 m height, 1.20 m unrolled width and 1.45 m cylinder radius are proposed design dimensions. The original mesh has no declared physical units.
- The Python solver is not a validated reimplementation of Kangaroo.
- Native execution of `STRIA_Baseline_Output_Repair.gh` and confirmation of solver point ordering remain outstanding.
- No physical fabrication, structural analysis, material tests, daylight analysis, acoustic tests or user studies were performed.
- Closed/watertight topology does not prove that a swept mesh is free of all self-intersections or manufacturable.
- Mounting ties, frame and freestanding feet are modeled design concepts. Mechanical joints and stability are unverified.
- The growth run ends at a fixed iteration budget. Convergence was not established.
- A single alternate seed is a sensitivity check, not a statistically representative robustness study.

## Attribution

Cameron Hendey independently developed the original Grasshopper definition, informed by existing differential-growth examples. The redevelopment's Python implementation, analysis, render workflow and documentation were generated with AI assistance under his approved Level 2 scope. Third-party precedent projects are not represented as his work.

The DejaVu fonts are bundled with their licence in `02_Visuals/Fonts`. Python dependencies retain their respective licences. All project-specific code in this package is editable.

## Crescent extension

The new showcase has four closed growth loops, 14,000 nodes and 198.45 m of centerline. It is a non-isometric remapping of the benchmark curve. Its clearance, curvature and physical support are not validated. Collage renders are artistic interpretations; exact model views and native geometry establish dimensions. See Visual_Revision.md for details.
