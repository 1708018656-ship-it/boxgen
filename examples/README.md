# Examples

Sample outputs from `boxgen` and a small preview helper.

| File | How it was made |
|---|---|
| `open_box_100x100x50.stl` | `boxgen open --width 100 --depth 100 --height 50 --wall 2 -o open_box_100x100x50.stl` |
| `closed_box_100x100x7.stl` | `boxgen closed --width 100 --depth 100 --height 7 -o closed_box_100x100x7.stl` |
| `lid_100x100.stl` | `boxgen lid --width 100 --depth 100 --skirt 5 --clearance 0.3 -o lid_100x100.stl` |
| `open_box_preview.png` | Render of the open box (see below) |

## Regenerate STLs

From the repo root (after `pip install -e .`):

```bash
boxgen open   --width 100 --depth 100 --height 50 --wall 2 -o examples/open_box_100x100x50.stl
boxgen closed --width 100 --depth 100 --height 7          -o examples/closed_box_100x100x7.stl
boxgen lid    --width 100 --depth 100 --skirt 5 --clearance 0.3 -o examples/lid_100x100.stl
```

## Preview image

Needs the optional preview extra:

```bash
pip install -e ".[preview]"
python examples/render_preview.py
# writes examples/open_box_preview.png
```

Open the `.stl` files in any slicer (PrusaSlicer, Cura, Bambu Studio, …) or upload to a print service to confirm they pass manifold / volume checks.
