"""Command line interface: ``boxgen {closed,open,lid} ...``."""
from __future__ import annotations

import argparse
import sys

from . import __version__
from .shapes import closed_box, lid, open_box


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="boxgen", description="Generate watertight STL boxes (mm).")
    p.add_argument("--version", action="version", version=f"boxgen {__version__}")
    sub = p.add_subparsers(dest="shape", required=True)

    def common(sp, default_out):
        sp.add_argument("-o", "--output", default=default_out, help="output STL path")
        sp.add_argument("--ascii", action="store_true", help="write ASCII STL instead of binary")
        sp.add_argument("--max-volume", type=float, metavar="CM3",
                        help="fail (exit 2) if material volume exceeds this (e.g. JLCPCB limits)")

    c = sub.add_parser("closed", help="solid cuboid")
    c.add_argument("--width", type=float, required=True)
    c.add_argument("--depth", type=float, required=True)
    g = c.add_mutually_exclusive_group(required=True)
    g.add_argument("--height", type=float)
    g.add_argument("--volume", type=float, metavar="CM3", help="solve height for this volume")
    common(c, "closed_box.stl")

    o = sub.add_parser("open", help="open-top hollow container")
    o.add_argument("--width", type=float, required=True)
    o.add_argument("--depth", type=float, required=True)
    g = o.add_mutually_exclusive_group(required=True)
    g.add_argument("--height", type=float)
    g.add_argument("--volume", type=float, metavar="CM3", help="solve height for this material volume")
    o.add_argument("--wall", type=float, default=2.0)
    o.add_argument("--floor", type=float, help="floor thickness (default = wall)")
    o.add_argument("--inner", action="store_true", help="width/depth/height are cavity dims")
    common(o, "open_box.stl")

    lp = sub.add_parser("lid", help="slip-over lid for an open box")
    lp.add_argument("--width", type=float, required=True, help="box OUTER width")
    lp.add_argument("--depth", type=float, required=True, help="box OUTER depth")
    lp.add_argument("--wall", type=float, default=2.0)
    lp.add_argument("--top", type=float, help="top plate thickness (default = wall)")
    lp.add_argument("--skirt", type=float, default=5.0)
    lp.add_argument("--clearance", type=float, default=0.3)
    common(lp, "lid.stl")

    a = p.parse_args(argv)
    try:
        if a.shape == "closed":
            m = closed_box(a.width, a.depth, a.height, volume_cm3=a.volume)
        elif a.shape == "open":
            m = open_box(a.width, a.depth, a.height, wall=a.wall, floor=a.floor,
                         volume_cm3=a.volume, inner=a.inner)
        else:
            m = lid(a.width, a.depth, wall=a.wall, top=a.top, skirt=a.skirt, clearance=a.clearance)
    except ValueError as e:
        p.error(str(e))
    info = m.check()
    lo, hi = m.bounds
    m.to_stl(a.output, ascii=a.ascii)
    print(f"wrote {a.output}")
    print(f"  size       : {hi[0]-lo[0]:g} x {hi[1]-lo[1]:g} x {hi[2]-lo[2]:g} mm")
    print(f"  volume     : {info['volume_cm3']:.3f} cm^3")
    print(f"  triangles  : {info['triangles']}  watertight={info['watertight']}  outward={info['outward']}")
    if a.max_volume is not None and info["volume_cm3"] > a.max_volume:
        print(f"ERROR: volume exceeds --max-volume {a.max_volume}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
