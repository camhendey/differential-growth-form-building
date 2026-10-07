# Visual redevelopment / torqued crescent

The crescent replaces the rectangular screen as the principal spatial showcase. The screen remains the controlled comparison rig. Both use the saved focused growth result; the crescent repeats that result across four parameter strips and maps each strip into a common flared, torqued host.

## Implemented geometry

`showcase.py` defines the host explicitly. For s=(u+0.6)/1.2 and t=v/1.8:

- angle = (-140 + 280s + 38t) degrees
- radius = 1.5 + 0.65t² + 0.20 sin(2πs)t metres
- height = 2.6 + 0.65 sin²(πs) + 0.25 sin(2πs) metres
- position = (radius sin(angle), radius cos(angle), 0.12 + t height)

The focused UV curve is repeated in four consecutive u strips, each 0.3 units wide. Each remains a separate closed loop. All four loops together contain 14,000 nodes and 198.45 m of polygonal centerline. The centerline bounds are 4.13 x 4.21 x 2.91 m, excluding frame and tube radius. The perimeter reaches higher than the strand. Tube diameter is a proposed 16 mm; perimeter diameter is 46 mm.

The mapping is not isometric. Segment stretch relative to the original saved UV curve ranges from 1.19 to 2.80 across all four strips. This is explicitly a geometric remapping, not a new differential-growth simulation on the crescent. The cylinder's openness, clearances and curvature statistics do not apply. New collision, curvature, support, joint and structural evaluation would be needed before physical development. Perimeter and curves are modeled; connections are not engineered or modeled for this showcase.

## Visual provenance

- `crescent_render.png`: exact exported geometry rendered using Mitsuba.
- `crescent_geometry.png` and `crescent_atlas.svg/png`: generated directly from saved mapped centerlines and host coordinates.
- `Showcase_Courtyard.png` and `Showcase_Interior.png`: interpretive AI-generated architectural collages guided by the model and user-supplied visual references. Context, figures, material appearance, shadows, exact strand placement and apparent scale are illustrative. They are not measured views, fabrication evidence or site proposals.
- The two final prompts and the interior refinement prompt are retained in `Art_Direction_Prompts.json`. Built-in image generation was used. Image generation is not deterministically reproducible from a prompt.
- Existing benchmark data is unchanged. Benchmark plots retain their original datasets, with a new sage/copper palette and field/curve overlays.

## Reproduction

Run `python showcase.py` followed by `python render_crescent.py` from the Code folder with the packaged requirements installed. These create the new Rhino model, mesh exports, saved coordinates, geometric record and exact model views. Run `python figures.py`, then `python build_pdf.py` to regenerate the portfolio using the supplied collage PNGs. Finally run `python package_project.py` to rebuild the archive.

## Quality pass

The first interior collage used overly broad ribbon sections and heavy dark corners. A deliberate refinement replaced them with round filaments and lighter paper edges. The host atlas was corrected to draw open isocurves without false closing chords. The exact render was corrected to hide the area emitter from the camera. These refinements preserve the separation between evocative imagery and geometry evidence.
