from pathlib import Path

from numpy import dtype, float64, ndarray, zeros_like
from pandas import DataFrame, read_csv
from whitecanvas import new_canvas

_parent_dir = Path(__file__).resolve().parent
assets_dir_0416 = _parent_dir / ".." / "0416" / "assets"

float1DArr = ndarray[float, dtype[float64]]


def calc_freq(data: DataFrame) -> float:
    t = data["t"].to_numpy()
    total_t: float = t[-1] - t[0]
    n: int = len(t)
    f: float = n / total_t

    print(f"{total_t=}, {n=}, {f=} Hz")
    return f


def integrate(
    data: float1DArr,
    dt: float,
) -> float1DArr:
    result = zeros_like(data)
    for i in range(1, len(data)):
        result[i] = result[i - 1] + (data[i] + data[i - 1]) * dt / 2
    return result


def show_graph(
    t: float1DArr,
    dx: float1DArr,
    dy: float1DArr,
    dz: float1DArr,
) -> None:
    canvas = new_canvas("pyqtgraph")
    canvas.add_line(t, dx, name="X-axis")
    canvas.add_line(t, dy, name="Y-axis")
    canvas.add_line(t, dz, name="Z-axis")
    canvas.add_legend(location="right_side_top")
    canvas.show(block=True)


def data_1_cumsum() -> None:
    data = read_csv(assets_dir_0416 / "1.csv")
    f = calc_freq(data)

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

    show_graph(t, dx, dy, dz)


def data_2_cumsum() -> None:
    data = read_csv(assets_dir_0416 / "2.csv")
    f = calc_freq(data)

    t_start = 1.5
    t_end = 2.8
    data = data[(data["t"] >= t_start) & (data["t"] <= t_end)]
    x = data["x"].to_numpy()
    y = data["y"].to_numpy()
    z = data["z"].to_numpy()
    t = data["t"].to_numpy()

    dt = 1 / f
    dx = (x.cumsum() * dt).cumsum() * dt
    dy = (y.cumsum() * dt).cumsum() * dt
    dz = (z.cumsum() * dt).cumsum() * dt

    show_graph(t, dx, dy, dz)


def data_1_integrate() -> None:
    data = read_csv(assets_dir_0416 / "1.csv")
    f = calc_freq(data)

    t_start = 1.11
    t_end = 1.6
    data = data[(data["t"] >= t_start) & (data["t"] <= t_end)]
    x = data["x"].to_numpy()
    y = data["y"].to_numpy()
    z = data["z"].to_numpy()
    t = data["t"].to_numpy()

    dt = 1 / f
    dx = integrate(integrate(x, dt), dt)
    dy = integrate(integrate(y, dt), dt)
    dz = integrate(integrate(z, dt), dt)

    show_graph(t, dx, dy, dz)


def data_2_integrate() -> None:
    data = read_csv(assets_dir_0416 / "2.csv")
    f = calc_freq(data)

    t_start = 1.5
    t_end = 2.8
    data = data[(data["t"] >= t_start) & (data["t"] <= t_end)]
    x = data["x"].to_numpy()
    y = data["y"].to_numpy()
    z = data["z"].to_numpy()
    t = data["t"].to_numpy()

    dt = 1 / f
    dx = integrate(integrate(x, dt), dt)
    dy = integrate(integrate(y, dt), dt)
    dz = integrate(integrate(z, dt), dt)

    show_graph(t, dx, dy, dz)


if __name__ == "__main__":
    # data_1_cumsum()
    # data_2_cumsum()
    # data_1_integrate()
    data_2_integrate()
