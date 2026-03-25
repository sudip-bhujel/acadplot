import os
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

from .draw import draw_bar
from .utils import colors
from .styles import configure_plot_style


def plot_bar(
    bars: List[Tuple[List[float], List[float], str | int, str]],
    location: str,
    fig_size: Tuple[float, float] = (3.0, 2.0),
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    xticklabels: Optional[List[str]] = None,
    rotation: float = 0.0,
    font_size: float = 6.0,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.35,
    fname: Optional[str] = "bar_plot.pdf",
):
    """Plot a bar chart with a legend.

    Args:
        bars (List[Tuple[List[float], List[float], str | int, str]]): List of bars,
            each defined by x positions, y values, color name or index, and label.
        location (str): Location of the legend.
        fig_size (Tuple[float, float], optional): Figure size. Defaults to (3, 2).
        label (Tuple[str, str], optional): Labels for the x and y axes. Defaults to ("x-label", "y-label").
        ax (Optional[plt.Axes], optional): Axes to plot on. Creates new if None. Defaults to None.
        xticklabels (Optional[List[str]], optional): Labels for x-axis ticks. Defaults to None.
        rotation (float, optional): Rotation angle for x-tick labels. Defaults to 0.0.
        font_size (float, optional): Font size for the plot. Defaults to 6.0.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of the bars. Defaults to 0.35.
        fname (Optional[str], optional): Filename to save the plot. Defaults to "bar_plot.pdf".
    """
    if ax is None:
        plt.figure(figsize=fig_size)
        ax = plt.gca()

    plt.rc("font", family="serif", size=font_size)

    ax.set_xlabel(label[0], fontsize=font_size)
    ax.set_ylabel(label[1], fontsize=font_size)
    ax.grid(color="#aaaaaa", dashes=[5, 5], linewidth=0.3, axis="y")

    for bar in bars:
        draw_bar(ax, bar[0], bar[1], bar[2], bar[3], bar_width)

    plt.rc("text", usetex=False)
    legend = ax.legend(
        loc=location,
        prop=dict(size=font_size, family="Fantasque Sans Mono"),
        framealpha=0.6,
        ncols=ncols,
        columnspacing=columnspacing,
    )
    legend.get_frame().set_linewidth(0.2)
    plt.rc("text", usetex=True)

    if xticklabels is not None:
        ax.set_xticks(bar[0])
        ax.set_xticklabels(xticklabels, rotation=rotation, fontsize=font_size)

    ax.tick_params(axis="both", labelsize=font_size)

    if fname:
        plt.tight_layout(pad=0.2)
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        plt.savefig(fname, dpi=300)


def plot_grouped_bar(
    groups: List[Tuple[str, List[Tuple[float, str | int, str]]]],
    location: str,
    fig_size: Tuple[float, float] = (3.5, 2.0),
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    rotation: float = 0.0,
    font_size: float = 6.0,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.25,
    fname: Optional[str] = "grouped_bar_plot.pdf",
):
    """Plot a grouped bar chart with multiple bars per group.

    Args:
        groups (List[Tuple[str, List[Tuple[float, str | int, str]]]]): List of groups,
            each defined by group name and a list of (value, color_key, label) tuples.
        location (str): Location of the legend.
        fig_size (Tuple[float, float], optional): Figure size. Defaults to (3.5, 2).
        label (Tuple[str, str], optional): Labels for the x and y axes. Defaults to ("x-label", "y-label").
        ax (Optional[plt.Axes], optional): Axes to plot on. Creates new if None. Defaults to None.
        rotation (float, optional): Rotation angle for x-tick labels. Defaults to 0.0.
        font_size (float, optional): Font size for the plot. Defaults to 6.0.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of each bar. Defaults to 0.25.
        fname (Optional[str], optional): Filename to save the plot. Defaults to "grouped_bar_plot.pdf".
    """
    if ax is None:
        plt.figure(figsize=fig_size)
        ax = plt.gca()

    plt.rc("font", family="serif", size=font_size)

    ax.set_xlabel(label[0], fontsize=font_size)
    ax.set_ylabel(label[1], fontsize=font_size)
    ax.grid(color="#aaaaaa", dashes=[5, 5], linewidth=0.3, axis="y")

    n_bars = len(groups[0][1]) if groups else 0
    group_positions = range(len(groups))
    group_step = 1.0

    for bar_idx in range(n_bars):
        positions = [
            pos + (bar_idx - n_bars / 2 + 0.5) * bar_width
            for pos in group_positions
        ]
        values = [group[1][bar_idx][0] for group in groups]
        color_key = groups[0][1][bar_idx][1]
        bar_label = groups[0][1][bar_idx][2]
        draw_bar(ax, positions, values, color_key, bar_label, bar_width)

    ax.set_xticks(list(group_positions))
    ax.set_xticklabels([g[0] for g in groups], rotation=rotation, fontsize=font_size)

    plt.rc("text", usetex=False)
    legend = ax.legend(
        loc=location,
        prop=dict(size=font_size, family="Fantasque Sans Mono"),
        framealpha=0.6,
        ncols=ncols,
        columnspacing=columnspacing,
    )
    legend.get_frame().set_linewidth(0.2)
    plt.rc("text", usetex=True)

    ax.tick_params(axis="both", labelsize=font_size)

    if fname:
        plt.tight_layout(pad=0.2)
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        plt.savefig(fname, dpi=300)


def plot_stacked_bar(
    categories: List[str],
    stacks: List[Tuple[List[float], str | int, str]],
    location: str,
    fig_size: Tuple[float, float] = (3.0, 2.0),
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    rotation: float = 0.0,
    font_size: float = 6.0,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.35,
    fname: Optional[str] = "stacked_bar_plot.pdf",
):
    """Plot a stacked bar chart.

    Args:
        categories (List[str]): Category labels for the x-axis.
        stacks (List[Tuple[List[float], str | int, str]]): List of stacks,
            each defined by values (one per category), color_key, and label.
        location (str): Location of the legend.
        fig_size (Tuple[float, float], optional): Figure size. Defaults to (3, 2).
        label (Tuple[str, str], optional): Labels for the x and y axes. Defaults to ("x-label", "y-label").
        ax (Optional[plt.Axes], optional): Axes to plot on. Creates new if None. Defaults to None.
        rotation (float, optional): Rotation angle for x-tick labels. Defaults to 0.0.
        font_size (float, optional): Font size for the plot. Defaults to 6.0.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of the bars. Defaults to 0.35.
        fname (Optional[str], optional): Filename to save the plot. Defaults to "stacked_bar_plot.pdf".
    """
    if ax is None:
        plt.figure(figsize=fig_size)
        ax = plt.gca()

    plt.rc("font", family="serif", size=font_size)

    ax.set_xlabel(label[0], fontsize=font_size)
    ax.set_ylabel(label[1], fontsize=font_size)
    ax.grid(color="#aaaaaa", dashes=[5, 5], linewidth=0.3, axis="y")

    x_positions = range(len(categories))

    for stack in stacks:
        values = stack[0]
        color_key = stack[1]
        stack_label = stack[2]

        if isinstance(color_key, int):
            color = list(colors.values())[color_key]
        elif isinstance(color_key, str):
            color = colors[color_key]

        ax.bar(
            x_positions,
            values,
            bar_width,
            bottom=None,
            color=color,
            edgecolor=color,
            alpha=0.8,
            label=stack_label,
        )

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(categories, rotation=rotation, fontsize=font_size)

    plt.rc("text", usetex=False)
    legend = ax.legend(
        loc=location,
        prop=dict(size=font_size, family="Fantasque Sans Mono"),
        framealpha=0.6,
        ncols=ncols,
        columnspacing=columnspacing,
    )
    legend.get_frame().set_linewidth(0.2)
    plt.rc("text", usetex=True)

    ax.tick_params(axis="both", labelsize=font_size)

    if fname:
        plt.tight_layout(pad=0.2)
        os.makedirs(os.path.dirname(fname), exist_ok=True)
        plt.savefig(fname, dpi=300)


if __name__ == "__main__":
    configure_plot_style()

    # Bar plot example
    bar_data: List[Tuple[List[float], List[float], str | int, str]] = [
        ([0, 1, 2, 3], [10, 20, 15, 25], "blue", "Bar A"),
        ([0, 1, 2, 3], [8, 15, 12, 20], "orange", "Bar B"),
    ]
    plot_bar(
        bar_data,
        "upper left",
        xticklabels=["A", "B", "C", "D"],
        fname="examples/bar_plot.png",
        font_size=8,
    )

    # Grouped bar plot example
    grouped_data: List[Tuple[str, List[Tuple[float, str | int, str]]]] = [
        ("Model X", [(10, "blue", "Train"), (8, "orange", "Val")]),
        ("Model Y", [(15, "blue", "Train"), (12, "orange", "Val")]),
        ("Model Z", [(12, "blue", "Train"), (14, "orange", "Val")]),
    ]
    plot_grouped_bar(
        grouped_data,
        "upper left",
        fname="examples/grouped_bar_plot.png",
        font_size=8,
    )

    # Stacked bar plot example
    categories = ["Dataset A", "Dataset B", "Dataset C"]
    stacked_data: List[Tuple[List[float], str | int, str]] = [
        ([10, 20, 15], "blue", "Method A"),
        ([5, 10, 8], "orange", "Method B"),
        ([3, 5, 4], "green", "Method C"),
    ]
    plot_stacked_bar(
        categories,
        stacked_data,
        "upper left",
        fname="examples/stacked_bar_plot.png",
        font_size=8,
    )
