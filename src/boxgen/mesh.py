"""Minimal triangle mesh with binary/ASCII STL I/O and validation."""
from __future__ import annotations

import struct
from collections import Counter
from dataclasses import dataclass, field

Vec = tuple[float, float, float]


def _normal(a: Vec, b: Vec, c: Vec) -> Vec:
    ux, uy, uz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    wx, wy, wz = c[0] - a[0], c[1] - a[1], c[2] - a[2]
    n = (uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx)
    length = sum(x * x for x in n) ** 0.5
    return (0.0, 0.0, 0.0) if length == 0 else tuple(x / length for x in n)


@dataclass
class Mesh:
    vertices: list[Vec] = field(default_factory=list)
    faces: list[tuple[int, int, int]] = field(default_factory=list)

    def quad(self, a: int, b: int, c: int, d: int) -> None:
        """Add quad a-b-c-d (counter-clockwise seen from outside)."""
        self.faces += [(a, b, c), (a, c, d)]

    # ---- metrics -------------------------------------------------------
    @property
    def volume(self) -> float:
        """Signed volume in mm^3 (positive when normals point outward)."""
        v6 = 0.0
        for i, j, k in self.faces:
            a, b, c = self.vertices[i], self.vertices[j], self.vertices[k]
            v6 += (a[0] * (b[1] * c[2] - b[2] * c[1])
                   - a[1] * (b[0] * c[2] - b[2] * c[0])
                   + a[2] * (b[0] * c[1] - b[1] * c[0]))
        return v6 / 6.0

    @property
    def bounds(self) -> tuple[Vec, Vec]:
        xs, ys, zs = zip(*self.vertices)
        return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

    def check(self) -> dict:
        """Watertight (each edge in 2 faces), consistent winding, outward."""
        directed = Counter()
        for f in self.faces:
            for n in range(3):
                directed[(f[n], f[(n + 1) % 3])] += 1
        consistent = all(c == 1 for c in directed.values())
        watertight = consistent and all((q, p) in directed for p, q in directed)
        return {
            "triangles": len(self.faces),
            "watertight": watertight,
            "winding_consistent": consistent,
            "outward": self.volume > 0,
            "volume_cm3": self.volume / 1000.0,
        }

    # ---- I/O -----------------------------------------------------------
    def to_stl(self, path: str, name: str = "boxgen", ascii: bool = False) -> None:
        tris = [tuple(self.vertices[i] for i in f) for f in self.faces]
        if ascii:
            with open(path, "w") as fh:
                fh.write(f"solid {name}\n")
                for a, b, c in tris:
                    fh.write("  facet normal %g %g %g\n    outer loop\n" % _normal(a, b, c))
                    for p in (a, b, c):
                        fh.write("      vertex %g %g %g\n" % p)
                    fh.write("    endloop\n  endfacet\n")
                fh.write(f"endsolid {name}\n")
            return
        with open(path, "wb") as fh:
            fh.write(name.encode()[:80].ljust(80, b"\x00"))
            fh.write(struct.pack("<I", len(tris)))
            for a, b, c in tris:
                fh.write(struct.pack("<12fH", *_normal(a, b, c), *a, *b, *c, 0))

    @classmethod
    def from_binary_stl(cls, path: str) -> "Mesh":
        """Read a binary STL, merging identical vertices."""
        with open(path, "rb") as fh:
            data = fh.read()
        (count,) = struct.unpack_from("<I", data, 80)
        if len(data) != 84 + 50 * count:
            raise ValueError("not a valid binary STL (size mismatch)")
        m, index = cls(), {}
        for t in range(count):
            vals = struct.unpack_from("<12f", data, 84 + 50 * t)
            ids = []
            for p in (vals[3:6], vals[6:9], vals[9:12]):
                if p not in index:
                    index[p] = len(m.vertices)
                    m.vertices.append(p)
                ids.append(index[p])
            m.faces.append(tuple(ids))
        return m
