import struct

import pytest

from boxgen import Mesh, closed_box, lid, open_box
from boxgen.cli import main


def ok(m):
    c = m.check()
    assert c["watertight"] and c["winding_consistent"] and c["outward"]
    return c


def test_closed_box_matches_original():
    m = closed_box(100, 100, 7)
    c = ok(m)
    assert c["triangles"] == 12
    assert c["volume_cm3"] == pytest.approx(70.0)
    assert m.bounds == ((0, 0, 0), (100, 100, 7))


def test_closed_box_from_volume():
    m = closed_box(100, 100, volume_cm3=70)
    assert m.bounds[1][2] == pytest.approx(7)


def test_open_box_matches_original():
    m = open_box(100, 100, 50, wall=2, floor=2)
    c = ok(m)
    assert c["triangles"] == 28
    assert c["volume_cm3"] == pytest.approx((100 * 100 * 50 - 96 * 96 * 48) / 1000)
    assert m.bounds == ((0, 0, 0), (100, 100, 50))


def test_open_box_inner_and_volume():
    m = open_box(50, 30, 20, wall=1.5, floor=3, inner=True)
    ok(m)
    assert m.bounds[1] == pytest.approx((53, 33, 23))
    t = open_box(100, 100, wall=2, volume_cm3=60)
    assert ok(t)["volume_cm3"] == pytest.approx(60)


def test_lid_fits():
    m = lid(100, 100, wall=2, clearance=0.3, skirt=5)
    ok(m)
    assert m.bounds[1] == pytest.approx((104.6, 104.6, 7))


@pytest.mark.parametrize("kw", [dict(wall=60), dict(height=1, floor=2), dict(height=-1)])
def test_invalid(kw):
    args = dict(width=100, depth=100, height=10)
    args.update(kw)
    with pytest.raises(ValueError):
        open_box(**args)


@pytest.mark.parametrize("ascii", [False, True])
def test_stl_roundtrip(tmp_path, ascii):
    p = tmp_path / "b.stl"
    open_box(40, 30, 20).to_stl(str(p), ascii=ascii)
    if ascii:
        txt = p.read_text()
        assert txt.startswith("solid") and txt.count("facet normal") == 28
    else:
        data = p.read_bytes()
        assert struct.unpack_from("<I", data, 80)[0] == 28
        m = Mesh.from_binary_stl(str(p))
        ok(m)
        assert m.bounds[1] == pytest.approx((40, 30, 20))


def test_cli(tmp_path, capsys):
    out = tmp_path / "x.stl"
    assert main(["open", "--width", "100", "--depth", "100", "--height", "50", "-o", str(out)]) == 0
    assert out.stat().st_size == 84 + 50 * 28
    assert main(["closed", "--width", "100", "--depth", "100", "--height", "8",
                 "--max-volume", "70", "-o", str(out)]) == 2
