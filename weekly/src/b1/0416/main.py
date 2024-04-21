from pathlib import Path

import pandas as pd
from whitecanvas import new_canvas

_parent_dir = Path(__file__).resolve().parent
assets_dir = _parent_dir / "assets"

data = pd.read_csv(assets_dir / "1.csv")

t_start = 1.11
t_end = 1.6
data = data[(data["t"] >= t_start) & (data["t"] <= t_end)]
x = data["x"].to_numpy()
y = data["y"].to_numpy()
z = data["z"].to_numpy()
t = data["t"].to_numpy()

x = x.cumsum().cumsum()
y = y.cumsum().cumsum()
z = z.cumsum().cumsum()

canvas = new_canvas("pyqtgraph")
canvas.add_line(t, x, name="X-axis")
canvas.add_line(t, y, name="Y-axis")
canvas.add_line(t, z, name="Z-axis")
canvas.add_legend(location="right_side_top")
canvas.show(block=True)

# data 2

data = pd.read_csv(assets_dir / "2.csv")

t_start = 1.5
t_end = 2.8
data = data[(data["t"] >= t_start) & (data["t"] <= t_end)]
x = data["x"].to_numpy()
y = data["y"].to_numpy()
z = data["z"].to_numpy()
t = data["t"].to_numpy()

x = x.cumsum().cumsum()
y = y.cumsum().cumsum()
z = z.cumsum().cumsum()

canvas = new_canvas("pyqtgraph")
canvas.add_line(t, x, name="X-axis")
canvas.add_line(t, y, name="Y-axis")
canvas.add_line(t, z, name="Z-axis")
canvas.add_legend(location="right_side_top")
canvas.show(block=True)
