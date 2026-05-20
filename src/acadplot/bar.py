from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

from .draw import draw_bar, resolve_color_key, resolve_pattern_key
from .styles import (
    apply_axis_style,
    apply_grid,
    configure_plot_style,
    get_current_style,
)
from .utils import new_alpha, save, styled_legend


def _prepare_axes(ax, fig_size):
    if ax is None:
        return plt.subplots(figsize=fig_size)
    return ax.figure, ax


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


def _apply_bar_axis_style(ax, tick_size: float) -> None:
    ax.tick_params(axis="both", labelsize=tick_size)
    apply_axis_style(ax)
    ax.tick_params(axis="x", length=0)


def _parse_bar(bar):
    if len(bar) == 5:
        x, y, color_key, pattern_key, bar_label = bar
        return x, y, color_key, pattern_key, bar_label
    if len(bar) == 4:
        x, y, color_key, bar_label = bar
        return x, y, color_key, None, bar_label
    if len(bar) == 3:
        x, y, bar_label = bar
        return x, y, None, None, bar_label
    raise ValueError("Bar entries must be (x, y, color, label) or (x, y, label).")


def _parse_group_bar(entry):
    if len(entry) == 4:
        value, color_key, pattern_key, bar_label = entry
        return value, color_key, pattern_key, bar_label
    if len(entry) == 3:
        value, color_key, bar_label = entry
        return value, color_key, None, bar_label
    if len(entry) == 2:
        value, bar_label = entry
        return value, None, None, bar_label
    raise ValueError(
        "Grouped bar entries must be (value, color, label) or (value, label)."
    )


def _parse_stack(stack):
    if len(stack) == 4:
        values, color_key, pattern_key, stack_label = stack
        return values, color_key, pattern_key, stack_label
    if len(stack) == 3:
        values, color_key, stack_label = stack
        return values, color_key, None, stack_label
    if len(stack) == 2:
        values, stack_label = stack
        return values, None, None, stack_label
    raise ValueError("Stack entries must be (values, color, label) or (values, label).")


def _resolve_pattern(patterns, index: int, label: str, explicit_pattern):
    if explicit_pattern is not None:
        return resolve_pattern_key(explicit_pattern)
    if patterns is None:
        return None
    if isinstance(patterns, dict):
        return resolve_pattern_key(patterns.get(label))
    if not patterns:
        return None
    return resolve_pattern_key(patterns[index % len(patterns)])


def _add_legend(
    ax,
    location: str,
    legend_size: float,
    ncols: int,
    columnspacing: float,
    legend_outside: bool | str,
):
    return styled_legend(
        ax,
        location,
        legend_size=legend_size,
        ncols=ncols,
        columnspacing=columnspacing,
        legend_outside=legend_outside,
    )


def plot_bar(
    bars: List[Tuple],
    location: str,
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    xticklabels: Optional[List[str]] = None,
    rotation: float = 0.0,
    font_size: Optional[float] = None,
    label_size: Optional[float] = None,
    tick_size: Optional[float] = None,
    legend_size: Optional[float] = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.35,
    patterns: Optional[Sequence[str | int] | dict[str, str | int]] = None,
    grid: Optional[str] = None,
    fname: Optional[str] = "bar_plot.pdf",
    legend_outside: bool | str = False,
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
        font_size (float, optional): Base font size for labels, ticks, and legend. Defaults to the active style.
        label_size (float, optional): Axis label size. Defaults to font_size or the active style.
        tick_size (float, optional): Tick label size. Defaults to font_size or the active style.
        legend_size (float, optional): Legend text size. Defaults to font_size or the active style.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of the bars. Defaults to 0.35.
        grid (str, optional): Grid preset: "major-y", "major", "major-minor", or "none".
        fname (Optional[str], optional): Filename to save the plot. Defaults to "bar_plot.pdf".
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

    fig, ax = _prepare_axes(ax, fig_size)

    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=label_size)
    ax.set_ylabel(label[1], fontsize=label_size)
    apply_grid(ax, grid or str(style["bar_grid"]))

    for bar_idx, bar in enumerate(bars):
        x, y, color_key, pattern_key, bar_label = _parse_bar(bar)
        pattern = _resolve_pattern(patterns, bar_idx, bar_label, pattern_key)
        draw_bar(ax, x, y, color_key, bar_label, bar_width, pattern)

    _add_legend(ax, location, legend_size, ncols, columnspacing, legend_outside)

    if xticklabels is not None and bars:
        ax.set_xticks(bars[0][0])
        ax.set_xticklabels(xticklabels, rotation=rotation, fontsize=tick_size)

    _apply_bar_axis_style(ax, tick_size)

    if fname:
        save(fig, fname, close=False)

    return fig, ax


def plot_grouped_bar(
    groups: List[Tuple[str, List[Tuple]]],
    location: str,
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    rotation: float = 0.0,
    font_size: Optional[float] = None,
    label_size: Optional[float] = None,
    tick_size: Optional[float] = None,
    legend_size: Optional[float] = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.25,
    patterns: Optional[Sequence[str | int] | dict[str, str | int]] = None,
    grid: Optional[str] = None,
    fname: Optional[str] = "grouped_bar_plot.pdf",
    legend_outside: bool | str = False,
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
        font_size (float, optional): Base font size for labels, ticks, and legend. Defaults to the active style.
        label_size (float, optional): Axis label size. Defaults to font_size or the active style.
        tick_size (float, optional): Tick label size. Defaults to font_size or the active style.
        legend_size (float, optional): Legend text size. Defaults to font_size or the active style.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of each bar. Defaults to 0.25.
        grid (str, optional): Grid preset: "major-y", "major", "major-minor", or "none".
        fname (Optional[str], optional): Filename to save the plot. Defaults to "grouped_bar_plot.pdf".
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

    fig, ax = _prepare_axes(ax, fig_size)

    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=label_size)
    ax.set_ylabel(label[1], fontsize=label_size)
    apply_grid(ax, grid or str(style["bar_grid"]))

    n_bars = len(groups[0][1]) if groups else 0
    group_positions = range(len(groups))

    for bar_idx in range(n_bars):
        positions = [
            pos + (bar_idx - n_bars / 2 + 0.5) * bar_width for pos in group_positions
        ]
        values = [group[1][bar_idx][0] for group in groups]
        _, color_key, pattern_key, bar_label = _parse_group_bar(groups[0][1][bar_idx])
        pattern = _resolve_pattern(patterns, bar_idx, bar_label, pattern_key)
        draw_bar(ax, positions, values, color_key, bar_label, bar_width, pattern)

    ax.set_xticks(list(group_positions))
    ax.set_xticklabels([g[0] for g in groups], rotation=rotation, fontsize=tick_size)

    _add_legend(ax, location, legend_size, ncols, columnspacing, legend_outside)
    _apply_bar_axis_style(ax, tick_size)

    if fname:
        save(fig, fname, close=False)

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
    label_size: Optional[float] = None,
    tick_size: Optional[float] = None,
    legend_size: Optional[float] = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    bar_width: float = 0.35,
    patterns: Optional[Sequence[str | int] | dict[str, str | int]] = None,
    grid: Optional[str] = None,
    fname: Optional[str] = "stacked_bar_plot.pdf",
    legend_outside: bool | str = False,
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
        font_size (float, optional): Base font size for labels, ticks, and legend. Defaults to the active style.
        label_size (float, optional): Axis label size. Defaults to font_size or the active style.
        tick_size (float, optional): Tick label size. Defaults to font_size or the active style.
        legend_size (float, optional): Legend text size. Defaults to font_size or the active style.
        ncols (int, optional): Number of columns in the legend. Defaults to 1.
        columnspacing (float, optional): Spacing between legend columns. Defaults to 0.5.
        bar_width (float, optional): Width of the bars. Defaults to 0.35.
        grid (str, optional): Grid preset: "major-y", "major", "major-minor", or "none".
        fname (Optional[str], optional): Filename to save the plot. Defaults to "stacked_bar_plot.pdf".
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

    fig, ax = _prepare_axes(ax, fig_size)

    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=label_size)
    ax.set_ylabel(label[1], fontsize=label_size)
    apply_grid(ax, grid or str(style["bar_grid"]))

    x_positions = range(len(categories))
    bottoms = [0.0] * len(categories)

    for stack_idx, stack in enumerate(stacks):
        values, color_key, pattern_key, stack_label = _parse_stack(stack)
        color = resolve_color_key(color_key)
        pattern = _resolve_pattern(patterns, stack_idx, stack_label, pattern_key)
        bar_alpha = float(style["bar_alpha"])
        bar_edge_color = str(style["bar_edge_color"])
        color_kwargs = {"edgecolor": bar_edge_color}
        if color is not None:
            color_kwargs["facecolor"] = new_alpha(to_rgba(color), bar_alpha)
        container = ax.bar(
            x_positions,
            values,
            bar_width,
            bottom=bottoms,
            linewidth=float(style["bar_edge_width"]),
            hatch=pattern,
            label=stack_label,
            zorder=3,
            **color_kwargs,
        )
        for patch in container.patches:
            if color is None:
                patch.set_facecolor(
                    new_alpha(to_rgba(patch.get_facecolor()), bar_alpha)
                )
            patch.set_edgecolor(bar_edge_color)
            patch.set_alpha(None)
        bottoms = [bottom + value for bottom, value in zip(bottoms, values)]

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(categories, rotation=rotation, fontsize=tick_size)

    _add_legend(ax, location, legend_size, ncols, columnspacing, legend_outside)
    _apply_bar_axis_style(ax, tick_size)

    if fname:
        save(fig, fname, close=False)

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
