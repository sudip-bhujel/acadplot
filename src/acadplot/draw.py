from typing import List

from matplotlib.colors import is_color_like, to_rgba

from .styles import get_current_style
from .utils import colors, markers, new_alpha


def resolve_color_key(color_key: str | int | None) -> str | None:
    """Resolve an AcadPlot color key, raw Matplotlib color, or default cycle color."""
    if color_key is None:
        return None
    if isinstance(color_key, int):
        return list(colors.values())[color_key]
    if color_key in colors:
        return colors[color_key]
    if is_color_like(color_key):
        return color_key
    raise ValueError(
        f"Unknown color {color_key!r}. Use a theme color name, index, or Matplotlib color."
    )


def draw(
    ax,
    x: List[float],
    y: List[float],
    color_key: str | int | None,
    marker_key: str | int,
    label: str,
):
    """Draw a line with markers on the given axes.

    Args:
        ax: The axes to draw on.
        x (List[float]): x values.
        y (List[float]): y values.
        color_key (str | int | None): Color name, index, raw Matplotlib color,
            or None to use the active theme palette cycle.
        marker_key (str | int): Marker name or index.
        label (str): Label for the line.
    """
    color = resolve_color_key(color_key)

    if isinstance(marker_key, int):
        marker = list(markers.values())[marker_key]
    elif isinstance(marker_key, str):
        marker = markers[marker_key]

    style = get_current_style()
    marker_style, marker_size = marker
    color_kwargs = {"color": color} if color is not None else {}

    (line,) = ax.plot(
        x,
        y,
        marker=marker_style,
        markersize=marker_size * float(style["marker_scale"]),
        markeredgewidth=float(style["marker_edge_width"]),
        linewidth=float(style["line_width"]),
        label=label,
        zorder=3,
        **color_kwargs,
    )
    resolved_color = line.get_color()
    line.set_markerfacecolor(new_alpha(to_rgba(resolved_color), 0.3))
    line.set_markeredgecolor(resolved_color)


def draw_bar(
    ax,
    x: List[float],
    y: List[float],
    color_key: str | int | None,
    label: str,
    width: float = 0.35,
):
    """Draw a bar on the given axes.

    Args:
        ax: The axes to draw on.
        x (List[float]): x positions.
        y (List[float]): bar heights.
        color_key (str | int | None): Color name, index, raw Matplotlib color,
            or None to use the active theme palette cycle.
        label (str): Label for the bar.
        width (float): Bar width. Defaults to 0.35.
    """
    color = resolve_color_key(color_key)
    style = get_current_style()
    color_kwargs = {"color": color, "edgecolor": color} if color is not None else {}

    container = ax.bar(
        x,
        y,
        width,
        linewidth=float(style["bar_edge_width"]),
        alpha=float(style["bar_alpha"]),
        label=label,
        zorder=3,
        **color_kwargs,
    )
    if color is None:
        for patch in container.patches:
            patch.set_edgecolor(patch.get_facecolor())
