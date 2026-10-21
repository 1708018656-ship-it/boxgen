"""Parametric box shapes. All units are millimetres; origin at a bottom corner."""
from __future__ import annotations

from .mesh import Mesh


def _pos(**kw):
    for k, v in kw.items():
        if v <= 0:
            raise ValueError(f"{k} must be > 0 (got {v})")


def closed_box(width: float, depth: float, height: float | None = None,
               volume_cm3: float | None = None) -> Mesh:
    """Solid cuboid. Give `height`, or `volume_cm3` to solve height from it."""
    if height is None:
        if volume_cm3 is None:
            raise ValueError("need height or volume_cm3")
        height = volume_cm3 * 1000.0 / (width * depth)
    _pos(width=width, depth=depth, height=height)
    W, D, H = width, depth, height
    m = Mesh(vertices=[(0, 0, 0), (W, 0, 0), (W, D, 0), (0, D, 0),
                       (0, 0, H), (W, 0, H), (W, D, H), (0, D, H)])
    m.quad(0, 3, 2, 1)  # bottom
    m.quad(4, 5, 6, 7)  # top
    m.quad(0, 1, 5, 4); m.quad(1, 2, 6, 5); m.quad(2, 3, 7, 6); m.quad(3, 0, 4, 7)
    return m


def open_box(width: float, depth: float, height: float | None = None,
             wall: float = 2.0, floor: float | None = None,
             volume_cm3: float | None = None, inner: bool = False) -> Mesh:
    """Open-top hollow container (tray).

    width/depth/height are OUTER dimensions unless ``inner=True``, in which
    case width/depth/height describe the cavity. ``volume_cm3`` solves the
    outer height so the *material* volume equals the target.
    """
    floor = wall if floor is None else floor
    if inner:
        width, depth = width + 2 * wall, depth + 2 * wall
        if height is not None:
            height = height + floor
    _pos(width=width, depth=depth, wall=wall, floor=floor)
    W, D, T, B = width, depth, wall, floor
    iw, idp = W - 2 * T, D - 2 * T
    if iw <= 0 or idp <= 0:
        raise ValueError("wall too thick for footprint")
    if height is None:
        if volume_cm3 is None:
            raise ValueError("need height or volume_cm3")
        height = (volume_cm3 * 1000.0 - iw * idp * B) / (W * D - iw * idp)
    H = height
    if H <= B:
        raise ValueError(f"height ({H:.3f}) must exceed floor thickness ({B})")
    m = Mesh(vertices=[
        (0, 0, 0), (W, 0, 0), (W, D, 0), (0, D, 0),          # 0-3 outer bottom
        (0, 0, H), (W, 0, H), (W, D, H), (0, D, H),          # 4-7 outer top
        (T, T, H), (W - T, T, H), (W - T, D - T, H), (T, D - T, H),  # 8-11 inner top
        (T, T, B), (W - T, T, B), (W - T, D - T, B), (T, D - T, B),  # 12-15 inner floor
    ])
    m.quad(0, 3, 2, 1)                                      # outer bottom
    m.quad(0, 1, 5, 4); m.quad(1, 2, 6, 5); m.quad(2, 3, 7, 6); m.quad(3, 0, 4, 7)
    m.quad(4, 5, 9, 8); m.quad(5, 6, 10, 9); m.quad(6, 7, 11, 10); m.quad(7, 4, 8, 11)  # rim
    m.quad(12, 8, 9, 13); m.quad(13, 9, 10, 14); m.quad(14, 10, 11, 15); m.quad(15, 11, 8, 12)  # inner walls
    m.quad(12, 13, 14, 15)                                  # cavity floor
    return m


def lid(box_width: float, box_depth: float, wall: float = 2.0,
        top: float | None = None, skirt: float = 5.0,
        clearance: float = 0.3) -> Mesh:
    """Slip-over cap for an open box of outer size box_width x box_depth.

    Printed upside-down: it is an open box whose cavity is the box footprint
    plus ``clearance`` on each side, ``skirt`` mm deep.
    """
    top = wall if top is None else top
    return open_box(box_width + 2 * clearance, box_depth + 2 * clearance,
                    skirt, wall=wall, floor=top, inner=True)
