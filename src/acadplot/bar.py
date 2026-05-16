import os
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt

from .draw import draw_bar, resolve_color_key
from .styles import (
    apply_axis_style,
    apply_grid,
    apply_legend_style,
    configure_plot_style,
    get_current_style,
)


def _prepare_axes(ax, fig_size):
    if ax is None:
        return plt.subplots(figsize=fig_size)
    return ax.figure, ax


def _save_figure(fig, fname: str) -> None:
    fig.tight_layout(pad=0.2)
    directory = os.path.dirname(fname)
    if directory:
        os.makedirs(directory, exist_ok=True)
    fig.savefig(fname, dpi=300, bbox_inches="tight", pad_inches=0)


def _parse_bar(bar):
    if len(bar) == 4:
        x, y, color_key, bar_label = bar
        return x, y, color_key, bar_label
    if len(bar) == 3:
        x, y, bar_label = bar
        return x, y, None, bar_label
    raise ValueError("Bar entries must be (x, y, color, label) or (x, y, label).")


def _parse_group_bar(entry):
    if len(entry) == 3:
        value, color_key, bar_label = entry
        return value, color_key, bar_label
    if len(entry) == 2:
        value, bar_label = entry
        return value, None, bar_label
    raise ValueError(
        "Grouped bar entries must be (value, color, label) or (value, label)."
    )


def _parse_stack(stack):
    if len(stack) == 3:
        values, color_key, stack_label = stack
        return values, color_key, stack_label
    if len(stack) == 2:
        values, stack_label = stack
        return values, None, stack_label
    raise ValueError("Stack entries must be (values, color, label) or (values, label).")


def _add_legend(ax, location: str, font_size: float, ncols: int, columnspacing: float):
    style = get_current_style()
    legend = ax.legend(
        loc=location,
        prop=dict(size=font_size, family=str(style["font_family"])),
        frameon=bool(style["legend_frameon"]),
        framealpha=float(style["legend_framealpha"]),
        facecolor=str(style["legend_face_color"]),
        edgecolor=str(style["legend_edge_color"]),
        ncols=ncols,
        columnspacing=columnspacing,
    )
    apply_legend_style(legend)
    return legend


def plot_bar(
    bars: List[Tuple],
    location: str,
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    xticklabels: Optional[List[str]] = None,
    rotation: float = 0.0,
    font_size: Optional[float] = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.35,
    grid: Optional[str] = None,
    fname: Optional[str] = "bar_plot.pdf",
):
    """Plot a bar chart with a legend.

    Args:
        bars (List[Tuple]): List of bars, each defined by x positions, y values,
            optional color name/index/raw Matplotlib color, and label. Omit color
            to use the active theme palette cycle.
        location (str): Location of the legend.
        fig_size (Tuple[float, float], optional): Figure size. Defaults to the active style.
        label (Tuple[str, str], optional): Labels for the x and y axes. Defaults to ("x-label", "y-label").
        ax (Optional[plt.Axes], optional): Axes to plot on. Creates new if None. Defaults to None.
        xticklabels (Optional[List[str]], optional): Labels for x-axis ticks. Defaults to None.
        rotation (float, optional): Rotation angle for x-tick labels. Defaults to 0.0.
        font_size (float, optional): Font size for the plot. Defaults to the active style.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of the bars. Defaults to 0.35.
        grid (str, optional): Grid preset: "major-y", "major", "major-minor", or "none".
        fname (Optional[str], optional): Filename to save the plot. Defaults to "bar_plot.pdf".
    """
    style = get_current_style()
    if fig_size is None:
        fig_size = style["fig_size"]
    if font_size is None:
        font_size = float(style["font_size"])

    fig, ax = _prepare_axes(ax, fig_size)

    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=font_size)
    ax.set_ylabel(label[1], fontsize=font_size)
    apply_grid(ax, grid or str(style["bar_grid"]))

    for bar in bars:
        draw_bar(ax, *_parse_bar(bar), bar_width)

    _add_legend(ax, location, font_size, ncols, columnspacing)

    if xticklabels is not None and bars:
        ax.set_xticks(bars[0][0])
        ax.set_xticklabels(xticklabels, rotation=rotation, fontsize=font_size)

    ax.tick_params(axis="both", labelsize=font_size)
    apply_axis_style(ax)

    if fname:
        _save_figure(fig, fname)

    return fig, ax


def plot_grouped_bar(
    groups: List[Tuple[str, List[Tuple]]],
    location: str,
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    rotation: float = 0.0,
    font_size: Optional[float] = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.25,
    grid: Optional[str] = None,
    fname: Optional[str] = "grouped_bar_plot.pdf",
):
    """Plot a grouped bar chart with multiple bars per group.

    Args:
        groups (List[Tuple[str, List[Tuple]]]): List of groups, each defined by
            group name and a list of (value, optional color, label) tuples. Omit
            color to use the active theme palette cycle.
        location (str): Location of the legend.
        fig_size (Tuple[float, float], optional): Figure size. Defaults to the active style.
        label (Tuple[str, str], optional): Labels for the x and y axes. Defaults to ("x-label", "y-label").
        ax (Optional[plt.Axes], optional): Axes to plot on. Creates new if None. Defaults to None.
        rotation (float, optional): Rotation angle for x-tick labels. Defaults to 0.0.
        font_size (float, optional): Font size for the plot. Defaults to the active style.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of each bar. Defaults to 0.25.
        grid (str, optional): Grid preset: "major-y", "major", "major-minor", or "none".
        fname (Optional[str], optional): Filename to save the plot. Defaults to "grouped_bar_plot.pdf".
    """
    style = get_current_style()
    if fig_size is None:
        fig_size = style["fig_size"]
    if font_size is None:
        font_size = float(style["font_size"])

    fig, ax = _prepare_axes(ax, fig_size)

    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=font_size)
    ax.set_ylabel(label[1], fontsize=font_size)
    apply_grid(ax, grid or str(style["bar_grid"]))

    n_bars = len(groups[0][1]) if groups else 0
    group_positions = range(len(groups))

    for bar_idx in range(n_bars):
        positions = [
            pos + (bar_idx - n_bars / 2 + 0.5) * bar_width for pos in group_positions
        ]
        values = [group[1][bar_idx][0] for group in groups]
        _, color_key, bar_label = _parse_group_bar(groups[0][1][bar_idx])
        draw_bar(ax, positions, values, color_key, bar_label, bar_width)

    ax.set_xticks(list(group_positions))
    ax.set_xticklabels([g[0] for g in groups], rotation=rotation, fontsize=font_size)

    _add_legend(ax, location, font_size, ncols, columnspacing)
    ax.tick_params(axis="both", labelsize=font_size)
    apply_axis_style(ax)

    if fname:
        _save_figure(fig, fname)

    return fig, ax


def plot_stacked_bar(
    categories: List[str],
    stacks: List[Tuple],
    location: str,
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    rotation: float = 0.0,
    font_size: Optional[float] = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.35,
    grid: Optional[str] = None,
    fname: Optional[str] = "stacked_bar_plot.pdf",
):
    """Plot a stacked bar chart.

    Args:
        categories (List[str]): Category labels for the x-axis.
        stacks (List[Tuple]): List of stacks, each defined by values, optional
            color name/index/raw Matplotlib color, and label. Omit color to use
            the active theme palette cycle.
        location (str): Location of the legend.
        fig_size (Tuple[float, float], optional): Figure size. Defaults to the active style.
        label (Tuple[str, str], optional): Labels for the x and y axes. Defaults to ("x-label", "y-label").
        ax (Optional[plt.Axes], optional): Axes to plot on. Creates new if None. Defaults to None.
        rotation (float, optional): Rotation angle for x-tick labels. Defaults to 0.0.
        font_size (float, optional): Font size for the plot. Defaults to the active style.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of the bars. Defaults to 0.35.
        grid (str, optional): Grid preset: "major-y", "major", "major-minor", or "none".
        fname (Optional[str], optional): Filename to save the plot. Defaults to "stacked_bar_plot.pdf".
    """
    style = get_current_style()
    if fig_size is None:
        fig_size = style["fig_size"]
    if font_size is None:
        font_size = float(style["font_size"])

    fig, ax = _prepare_axes(ax, fig_size)

    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=font_size)
    ax.set_ylabel(label[1], fontsize=font_size)
    apply_grid(ax, grid or str(style["bar_grid"]))

    x_positions = range(len(categories))
    bottoms = [0.0] * len(categories)

    for stack in stacks:
        values, color_key, stack_label = _parse_stack(stack)
        color = resolve_color_key(color_key)
        color_kwargs = {"color": color, "edgecolor": color} if color is not None else {}
        container = ax.bar(
            x_positions,
            values,
            bar_width,
            bottom=bottoms,
            linewidth=float(style["bar_edge_width"]),
            alpha=float(style["bar_alpha"]),
            label=stack_label,
            zorder=3,
            **color_kwargs,
        )
        if color is None:
            for patch in container.patches:
                patch.set_edgecolor(patch.get_facecolor())
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(categories, rotation=rotation, fontsize=font_size)

    _add_legend(ax, location, font_size, ncols, columnspacing)
    ax.tick_params(axis="both", labelsize=font_size)
    apply_axis_style(ax)

    if fname:
        _save_figure(fig, fname)

    return fig, ax


if __name__ == "__main__":
    configure_plot_style()

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
