# boxgen

[English](#english) | [简体中文](#简体中文)

![open box preview](examples/open_box_preview.png)

## English

**boxgen** generates clean, watertight, manifold STL boxes for 3D printing — a solid
closed box, an open-top container (tray), and a matching slip-over lid. Pure Python,
zero runtime dependencies. Output passes common print-service checks (e.g. JLCPCB):
single shell, no reversed triangles, no bad edges, and you can enforce a maximum
material volume.

### Install

```bash
git clone https://github.com/1708018656-ship-it/boxgen && cd boxgen
pip install -e .            # add [dev] for pytest, [preview] for matplotlib
```

### CLI

```bash
# open-top container, outer 100x100x50 mm, 2 mm walls
boxgen open --width 100 --depth 100 --height 50 --wall 2 -o box.stl
# cavity of 50x30x20 mm, 1.5 mm walls, 3 mm floor
boxgen open --inner --width 50 --depth 30 --height 20 --wall 1.5 --floor 3 -o tray.stl
# solve the height so the material volume is exactly 60 cm³
boxgen open --width 100 --depth 100 --volume 60 -o box60.stl
# solid block of exactly 70 cm³ and fail if it exceeds 70 cm³
boxgen closed --width 100 --depth 100 --volume 70 --max-volume 70 -o block.stl
# lid that slips over a 100x100 box
boxgen lid --width 100 --depth 100 --skirt 5 --clearance 0.3 -o lid.stl
```

Also `python -m boxgen ...`, `--ascii` for ASCII STL, `boxgen <shape> -h` for help.

### Python API

```python
from boxgen import open_box, closed_box, lid

m = open_box(100, 100, 50, wall=2, floor=2)
print(m.check())        # {'triangles': 28, 'watertight': True, ..., 'volume_cm3': 57.632}
print(m.bounds)         # ((0, 0, 0), (100, 100, 50))
m.to_stl("box.stl")
```

### Parameters (mm)

| Shape | Parameter | Default | Meaning |
|---|---|---|---|
| all | `--width`, `--depth` | required | outer footprint (cavity if `--inner`; box outer size for `lid`) |
| closed/open | `--height` / `--volume` | one required | outer height, or target material volume in cm³ (height is solved) |
| open, lid | `--wall` | 2.0 | wall thickness |
| open | `--floor` | = wall | floor thickness |
| open | `--inner` | off | treat width/depth/height as cavity dimensions |
| lid | `--top` | = wall | top plate thickness |
| lid | `--skirt` | 5.0 | depth the lid overlaps the box |
| lid | `--clearance` | 0.3 | gap per side between box and lid |
| all | `--max-volume` | – | exit with code 2 if material volume (cm³) exceeds it |
| all | `-o`, `--ascii` | binary | output path / format |

### Roadmap

- Rounded corners / fillets
- Internal dividers (grid compartments)
- Inset (press-fit) lids and snap-fit tabs
- Text/label embossing
- 3MF export

## 简体中文

**boxgen** 用于生成干净、水密（流形）的 3D 打印 STL 盒子：实心封闭盒、开口收纳盒（托盘）以及配套的外扣盒盖。纯 Python 实现，无运行时依赖。输出满足常见打印服务（如嘉立创）检查：单壳体、无反向三角面、无坏边，并可限制最大材料体积。

### 安装

```bash
git clone https://github.com/1708018656-ship-it/boxgen && cd boxgen
pip install -e .            # [dev] 安装 pytest，[preview] 安装 matplotlib
```

### 命令行示例

```bash
boxgen open --width 100 --depth 100 --height 50 --wall 2 -o box.stl        # 外尺寸 100x100x50，壁厚 2
boxgen open --inner --width 50 --depth 30 --height 20 --floor 3 -o tray.stl # 按内腔尺寸
boxgen open --width 100 --depth 100 --volume 60 -o box60.stl               # 自动求高度使材料体积 = 60 cm³
boxgen closed --width 100 --depth 100 --volume 70 --max-volume 70 -o block.stl  # 体积超过 70 cm³ 则报错
boxgen lid --width 100 --depth 100 --skirt 5 --clearance 0.3 -o lid.stl    # 配套盒盖
```

### Python 接口

```python
from boxgen import open_box
m = open_box(100, 100, 50, wall=2, floor=2)
print(m.check())   # 水密性、法线方向、体积
m.to_stl("box.stl")
```

### 参数说明（单位 mm）

| 形状 | 参数 | 默认值 | 含义 |
|---|---|---|---|
| 全部 | `--width`、`--depth` | 必填 | 外部长宽（`--inner` 时为内腔；`lid` 时为盒子外尺寸） |
| closed/open | `--height` / `--volume` | 二选一 | 外高度，或目标材料体积 (cm³)，自动求解高度 |
| open、lid | `--wall` | 2.0 | 壁厚 |
| open | `--floor` | 同壁厚 | 底厚 |
| open | `--inner` | 关 | 长宽高按内腔尺寸计算 |
| lid | `--top` | 同壁厚 | 顶板厚度 |
| lid | `--skirt` | 5.0 | 盒盖套住盒子的深度 |
| lid | `--clearance` | 0.3 | 盒盖与盒子单边间隙 |
| 全部 | `--max-volume` | – | 材料体积超过该值 (cm³) 时以退出码 2 报错 |
| 全部 | `-o`、`--ascii` | 二进制 | 输出路径 / 格式 |

### 路线图

- 圆角
- 内部隔板（分格）
- 嵌入式盒盖、卡扣
- 文字浮雕
- 3MF 导出

## License / 许可证

MIT © 1708018656-ship-it. See [CONTRIBUTING.md](CONTRIBUTING.md).
