from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

from .draw import draw
from .styles import (
    apply_axis_style,
    apply_grid,
    configure_plot_style,
    get_current_style,
)
from .utils import save, styled_legend


def _parse_line(line):
    if len(line) == 5:
        x, y, color_key, marker_key, line_label = line
        return x, y, color_key, marker_key, line_label
    if len(line) == 4:
        x, y, marker_key, line_label = line
        return x, y, None, marker_key, line_label
    raise ValueError(
        "Line entries must be (x, y, color, marker, label) or (x, y, marker, label)."
    )


def _resolve_text_sizes(style, font_size, label_size, tick_size, legend_size):
    font_size_override = font_size
    if font_size is None:
        font_size = float(style["font_size"])
    if label_size is None:
        label_size = (
            font_size_override
            if font_size_override is not None
            else float(style["label_size"])
        )
    if tick_size is None:
        tick_size = (
            font_size_override
            if font_size_override is not None
            else float(style["tick_size"])
        )
    if legend_size is None:
        legend_size = (
            font_size_override
            if font_size_override is not None
            else float(style["legend_size"])
        )
    return font_size, label_size, tick_size, legend_size


def plot_line(
    lines: List[Tuple],
    location: str,
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    xticks: Optional[List[float] | range] = None,
    yticks: Optional[List[float] | range] = None,
    xstart: Optional[float] = None,
    ystart: Optional[float] = None,
    font_size: Optional[float] = None,
    label_size: Optional[float] = None,
    tick_size: Optional[float] = None,
    legend_size: Optional[float] = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    grid: Optional[str] = None,
    fname: Optional[str] = "plot.pdf",
    legend_outside: bool | str = False,
):
    """Plot multiple lines with markers and a legend.

    Args:
        lines (List[Tuple]): List of lines to plot, each defined by
            (x values, y values, color name/index, marker name/index, label)
            or (x values, y values, marker name/index, label). Omit color to
            use the active theme palette cycle.
        location (str): Location of the legend.
        fig_size (Tuple[float, float], optional): Figure size. Defaults to the active style.
        label (Tuple[str, str], optional): Labels for the x and y axes. Defaults to ("x-label", "y-label").
        ax (Optional[plt.Axes], optional): Axes to plot on. Creates new if None. Defaults to None.
        xticks (Optional[List[float] | range], optional): Custom x-axis ticks. Defaults to None.
        yticks (Optional[List[float] | range], optional): Custom y-axis ticks. Defaults to None.
        xstart (Optional[float], optional): Minimum x-axis value. Defaults to None.
        ystart (Optional[float], optional): Minimum y-axis value. Defaults to None.
        font_size (float, optional): Base font size for labels, ticks, and legend. Defaults to the active style.
        label_size (float, optional): Axis label size. Defaults to font_size or the active style.
        tick_size (float, optional): Tick label size. Defaults to font_size or the active style.
        legend_size (float, optional): Legend text size. Defaults to font_size or the active style.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        grid (str, optional): Grid preset: "major-y", "major", "major-minor", or "none".
        fname (Optional[str], optional): Filename to save the plot. Defaults to "plot.pdf".
    """
    style = get_current_style()
    if fig_size is None:
        fig_size = style["fig_size"]
    font_size, label_size, tick_size, legend_size = _resolve_text_sizes(
        style,
        font_size,
        label_size,
        tick_size,
        legend_size,
    )

    if ax is None:
        fig, ax = plt.subplots(figsize=fig_size)
    else:
        fig = ax.figure

    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=label_size)
    ax.set_ylabel(label[1], fontsize=label_size)
    apply_grid(ax, grid or str(style["line_grid"]))

    for line in lines:
        draw(ax, *_parse_line(line))

    styled_legend(
        ax,
        location,
        legend_size=legend_size,
        ncols=ncols,
        columnspacing=columnspacing,
        legend_outside=legend_outside,
    )

    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)

    ax.tick_params(axis="both", labelsize=tick_size)
    apply_axis_style(ax)

    if xstart is not None:
        ax.set_xlim(left=xstart)
    if ystart is not None:
        ax.set_ylim(bottom=ystart)

    if fname:
        save(fig, fname, close=False)

    return fig, ax


if __name__ == "__main__":
    configure_plot_style()
    data: List[Tuple[List[float], List[float], str | int, str | int, str]] = [
        ([10, 20, 30, 40, 50], [5, 10, 15, 20, 25], "blue", 8, "Method A"),
        (
            [10, 20, 30, 40, 50],
            [6, 11, 14, 18, 22],
            "orange",
            0,
            "Method B",
        ),
        (
            [10, 20, 30, 40, 50],
            [7, 9, 13, 19, 24],
            "green",
            1,
            "Method C",
        ),
    ]

    # Single plot usage (unchanged)
    plot_line(
        data,
        "upper left",
        ystart=min(min(y) for _, y, _, _, _ in data),
        yticks=range(0, 30, 5),
        fname="examples/plot.png",
        font_size=8,
    )

    # Subplot usage example
    fig, axes = plt.subplots(1, 2, figsize=(6, 2))
    plot_line(data, "upper left", ax=axes[0], yticks=range(0, 30, 5), fname=None)
    plot_line(data, "upper left", ax=axes[1], yticks=range(0, 30, 5), fname=None)
    plt.tight_layout(pad=0.2)
    plt.subplots_adjust(wspace=0.27)  # Add horizontal space between subplots
    save(fig, "examples/subplot.png")
