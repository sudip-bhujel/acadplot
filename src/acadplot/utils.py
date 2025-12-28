from typing import Iterable, List, Tuple


def blend_color(
    rgba1: Tuple[float, float, float, float], rgba2: Tuple[float, float, float, float]
) -> Tuple[float, float, float, float]:
    return (
        (rgba1[0] + rgba2[0]) / 2.0,
        (rgba1[1] + rgba2[1]) / 2.0,
        (rgba1[2] + rgba2[2]) / 2.0,
        (rgba1[3] + rgba2[3]) / 2.0,
    )


def new_alpha(
    c: tuple[float, float, float] | tuple[float, float, float, float],
    alpha: float,
) -> tuple[float, float, float, float]:
    return (c[0], c[1], c[2], alpha)


markers = {
    "square": ("s", 3.5),
    "triangle_up": ("^", 4),
    "pentagon": ("p", 5),
    "circle": ("o", 4),
    "star": ("*", 4.5),
    "plus_filled": ("P", 3.5),
    "triangle_down": ("v", 4),
    "diamond": ("D", 3),
    "x_filled": ("X", 3.5),
    "triangle_left": ("<", 4),
    "triangle_right": (">", 4),
    "thin_diamond": ("d", 3),
    "hexagon1": ("h", 4),
    "hexagon2": ("H", 4),
    "plus": ("+", 4),
    "x": ("x", 4),
    "vline": ("|", 4),
    "hline": ("_", 4),
    "point": (".", 2),
    "pixel": (",", 1),
    "tri_down": ("1", 4),
    "tri_up": ("2", 4),
    "tri_left": ("3", 4),
    "tri_right": ("4", 4),
    "octagon": ("8", 4),
    "none": ("", 0),
}

colors = {
    "blue": "#0173B2",
    "orange": "#DE8F05",
    "green": "#029E73",
    "purple": "#CC78BC",
    "brown": "#CA9161",
    "yellow": "#ECE133",
    "sky_blue": "#56B4E9",
    "gray": "#949494",
    "red": "#D55E00",
    "pink": "#CC79A7",
    "teal": "#009E73",
    "olive": "#808000",
    "navy": "#0072B2",
    "maroon": "#800000",
    "lime": "#00FF00",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "dark_gray": "#404040",
    "light_gray": "#D3D3D3",
}
