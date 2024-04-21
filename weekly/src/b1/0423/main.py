from pathlib import Path

import pandas as pd
from whitecanvas import new_canvas

_parent_dir = Path(__file__).resolve().parent
assets_dir_0416 = _parent_dir / ".." / "0416" / "assets"

data = pd.read_csv(assets_dir_0416 / "1.csv")

t = data["t"].to_numpy()
total_t: float = t[-1] - t[0]
n: int = len(t)
f: float = n / total_t

print(f"{total_t=}, {n=}, {f=} Hz")

t_start = 1.11
t_end = 1.6
data = data[(data["t"] >= t_start) & (data["t"] <= t_end)]
x = data["x"].to_numpy()
y = data["y"].to_numpy()
z = data["z"].to_numpy()
t = data["t"].to_numpy()

dt = 1 / f
dx = (x.cumsum() * dt).cumsum() * dt
dy = (y.cumsum() * dt).cumsum() * dt
dz = (z.cumsum() * dt).cumsum() * dt

canvas = new_canvas("pyqtgraph")
canvas.add_line(t, dx, name="X-axis")
canvas.add_line(t, dy, name="Y-axis")
canvas.add_line(t, dz, name="Z-axis")
canvas.add_legend(location="right_side_top")
canvas.show(block=True)
