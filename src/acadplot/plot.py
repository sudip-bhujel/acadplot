import os
from tkinter import font
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

from .utils import colors, markers, new_alpha


def configure_plot_style():
    """
    Configure global plot style settings.

    Uses LaTeX for text rendering and sets line widths for axes and ticks.
    """
    plt.rc("text", usetex=True)
    plt.rc("axes", linewidth=0.5)
    plt.rc("xtick.major", width=0.5)
    plt.rc("xtick.minor", width=0.3)
    plt.rc("ytick.major", width=0.5)
    plt.rc("ytick.minor", width=0.3)
    plt.rc("font", family="serif")


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


def plot_line(
    lines: List[Tuple[List[float], List[float], str | int, str | int, str]],
    location: str,
    fig_size: Tuple[float, float] = (3.0, 2.0),
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    xticks: Optional[List[float] | range] = None,
    yticks: Optional[List[float] | range] = None,
    xstart: Optional[float] = None,
    ystart: Optional[float] = None,
    font_size=6.0,
    ncols: int = 1,
    columnspacing: float = 0.5,
    fname: Optional[str] = "plot.pdf",
):
    """Plot multiple lines with markers and a legend.

    Args:
        lines (List[Tuple[List[float], List[float], str | int, str | int, str]]): List of lines to plot, each defined by x values, y values, color name or index, marker name or index, and label.
        location (str): Location of the legend.
        fig_size (Tuple[float, float], optional): Figure size. Defaults to (3, 2).
        label (Tuple[str, str], optional): Labels for the x and y axes. Defaults to ("x-label", "y-label").
        ax (Optional[plt.Axes], optional): Axes to plot on. Creates new if None. Defaults to None.
        xticks (Optional[List[float] | range], optional): Custom x-axis ticks. Defaults to None.
        yticks (Optional[List[float] | range], optional): Custom y-axis ticks. Defaults to None.
        xstart (Optional[float], optional): Minimum x-axis value. Defaults to None.
        ystart (Optional[float], optional): Minimum y-axis value. Defaults to None.
        font_size (float, optional): Font size for the plot. Defaults to 6.0.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        fname (Optional[str], optional): Filename to save the plot. Defaults to "plot.pdf".
    """
    if ax is None:
        plt.figure(figsize=fig_size)
        ax = plt.gca()

    plt.rc("font", family="serif", size=font_size)

    ax.set_xlabel(label[0], fontsize=font_size)
    ax.set_ylabel(label[1], fontsize=font_size)
    ax.grid(color="#aaaaaa", dashes=[5, 5], linewidth=0.3)

    for line in lines:
        draw(ax, line[0], line[1], line[2], line[3], line[4])

    # plt.rc("text", usetex=False)
    legend = ax.legend(
        loc=location,
        prop=dict(size=font_size, family="serif"),
        framealpha=0.6,
        ncols=ncols,
        columnspacing=columnspacing,
    )
    legend.get_frame().set_linewidth(0.2)
    # plt.rc("text", usetex=True)

    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)

    ax.tick_params(axis="both", labelsize=font_size)

    if xstart is not None:
        ax.set_xlim(left=xstart)
    if ystart is not None:
        ax.set_ylim(bottom=ystart)

    if fname:
        plt.tight_layout(pad=0.2)
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        plt.savefig(fname, dpi=300)


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
    plt.savefig("examples/subplot.png", dpi=300)

    # # Subplot usage example
    # fig, axes = plt.subplots(1, 2, figsize=(6, 2))
    # plot_line(data, "upper left", ax=axes[0], fname=None)
    # plot_line(data, "upper right", ax=axes[1], fname=None)

    # # Remove individual legends from subplots
    # axes[0].get_legend().remove()
    # axes[1].get_legend().remove()

    # # Get handles and labels from one of the subplots
    # handles, labels = axes[0].get_legend_handles_labels()

    # # Create a single legend at the bottom center
    # fig.legend(
    #     handles,
    #     labels,
    #     loc="lower center",
    #     bbox_to_anchor=(0.5, -0.1),
    #     prop=dict(size=6, family="DejaVu Serif"),
    #     framealpha=0.6,
    #     columnspacing=0.5,
    #     ncols=3,
    # )

    # plt.tight_layout(pad=0.2)
    # plt.subplots_adjust(wspace=0.27)  # Add horizontal space between subplots
    # plt.savefig("examples/subplots.pdf", bbox_inches="tight")
