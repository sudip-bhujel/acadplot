from typing import List

from matplotlib.colors import to_rgba

from .utils import colors, markers, new_alpha


def draw(
    ax,
    x: List[float],
    y: List[float],
    color_key: str | int,
    marker_key: str | int,
    label: str,
):
    """Draw a line with markers on the given axes.

    Args:
        ax: The axes to draw on.
        x (List[float]): x values.
        y (List[float]): y values.
        color_key (str | int): Color name or index of the line and markers.
        marker_key (str | int): Marker name or index.
        label (str): Label for the line.
    """
    if isinstance(color_key, int):
        color = list(colors.values())[color_key]
    elif isinstance(color_key, str):
        color = colors[color_key]

    if isinstance(marker_key, int):
        marker = list(markers.values())[marker_key]
    elif isinstance(marker_key, str):
        marker = markers[marker_key]

    marker_style, marker_size = marker

    ax.plot(
        x,
        y,
        marker=marker_style,
        markersize=marker_size,
        markeredgewidth=0.5,
        linewidth=0.3,
        markerfacecolor=new_alpha(to_rgba(color), 0.3),
        markeredgecolor=color,
        color=color,
        label=label,
    )


def draw_bar(
    ax,
    x: List[float],
    y: List[float],
    color_key: str | int,
    label: str,
    width: float = 0.35,
):
    """Draw a bar on the given axes.

    Args:
        ax: The axes to draw on.
        x (List[float]): x positions.
        y (List[float]): bar heights.
        color_key (str | int): Color name or index.
        label (str): Label for the bar.
        width (float): Bar width. Defaults to 0.35.
    """
    if isinstance(color_key, int):
        color = list(colors.values())[color_key]
    elif isinstance(color_key, str):
        color = colors[color_key]

    ax.bar(
        x,
        y,
        width,
        color=color,
        edgecolor=color,
        alpha=0.8,
        label=label,
    )
