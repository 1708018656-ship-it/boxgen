"""boxgen - parametric, watertight STL boxes for 3D printing (pure Python)."""
from .mesh import Mesh
from .shapes import closed_box, open_box, lid

__all__ = ["Mesh", "closed_box", "open_box", "lid"]
__version__ = "0.1.0"
