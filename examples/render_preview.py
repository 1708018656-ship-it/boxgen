"""Render a PNG preview of an STL with matplotlib: python render_preview.py in.stl out.png"""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from boxgen import Mesh

m = Mesh.from_binary_stl(sys.argv[1])
fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(projection="3d")
ax.add_collection3d(Poly3DCollection([[m.vertices[i] for i in f] for f in m.faces],
                                     facecolor="#4a90d9", edgecolor="#1b3a5c", linewidths=0.5, alpha=0.85))
lo, hi = m.bounds
s = max(h - l for l, h in zip(lo, hi))
ax.set_xlim(lo[0], lo[0] + s); ax.set_ylim(lo[1], lo[1] + s); ax.set_zlim(lo[2], lo[2] + s)
ax.set_xlabel("X (mm)"); ax.set_ylabel("Y (mm)"); ax.set_zlabel("Z (mm)")
ax.view_init(elev=30, azim=-60)
ax.set_title(sys.argv[1].split("/")[-1])
fig.tight_layout()
fig.savefig(sys.argv[2], dpi=120)
