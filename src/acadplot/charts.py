from itertools import cycle
from typing import List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch

from .draw import resolve_color_key
from .styles import apply_axis_style, apply_grid, apply_legend_style, get_current_style
from .utils import markers, new_alpha, save


def _prepare_axes(ax, fig_size):
    if ax is None:
        return plt.subplots(figsize=fig_size)
    return ax.figure, ax


def _resolve_marker(marker_key: str | int):
    if isinstance(marker_key, int):
        return list(markers.values())[marker_key]
    return markers[marker_key]


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


def _parse_xy_marker_series(series):
    if len(series) == 5:
        x, y, color_key, marker_key, series_label = series
        return x, y, color_key, marker_key, series_label
    if len(series) == 4:
        x, y, marker_key, series_label = series
        return x, y, None, marker_key, series_label
    raise ValueError(
        "Series entries must be (x, y, color, marker, label) or (x, y, marker, label)."
    )


def _parse_errorbar_series(series):
    if len(series) == 6:
        x, y, yerr, color_key, marker_key, series_label = series
        return x, y, yerr, color_key, marker_key, series_label
    if len(series) == 5:
        x, y, yerr, marker_key, series_label = series
        return x, y, yerr, None, marker_key, series_label
    raise ValueError(
        "Errorbar entries must be (x, y, yerr, color, marker, label) or "
        "(x, y, yerr, marker, label)."
    )


def _parse_box_group(group):
    if len(group) == 3:
        values, color_key, group_label = group
        return values, color_key, group_label
    if len(group) == 2:
        values, group_label = group
        return values, None, group_label
    raise ValueError("Box groups must be (values, color, label) or (values, label).")


def _add_legend(
    ax, location: str, legend_size: float, ncols: int, columnspacing: float
):
    style = get_current_style()
    legend = ax.legend(
        loc=location,
        prop=dict(size=legend_size, family=str(style["font_family"])),
        frameon=bool(style["legend_frameon"]),
        framealpha=float(style["legend_framealpha"]),
        facecolor=str(style["legend_face_color"]),
        edgecolor=str(style["legend_edge_color"]),
        ncols=ncols,
        columnspacing=columnspacing,
    )
    apply_legend_style(legend)
    return legend


def plot_scatter(
    series: List[Tuple],
    location: str = "best",
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    font_size: Optional[float] = None,
    label_size: Optional[float] = None,
    tick_size: Optional[float] = None,
    legend_size: Optional[float] = None,
    marker_size: Optional[float] = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    grid: Optional[str] = None,
    fname: Optional[str] = "scatter_plot.pdf",
):
    """Plot one or more scatter series."""
    style = get_current_style()
    if fig_size is None:
        fig_size = style["fig_size"]
    _, label_size, tick_size, legend_size = _resolve_text_sizes(
        style, font_size, label_size, tick_size, legend_size
    )
    if marker_size is None:
        marker_size = 28.0 * float(style["marker_scale"])

    fig, ax = _prepare_axes(ax, fig_size)
    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=label_size)
    ax.set_ylabel(label[1], fontsize=label_size)
    apply_grid(ax, grid or str(style["line_grid"]))

    palette_iter = cycle(style["palette"])
    for item in series:
        x, y, color_key, marker_key, series_label = _parse_xy_marker_series(item)
        color = resolve_color_key(color_key)
        if color is None:
            color = next(palette_iter)
        marker, _ = _resolve_marker(marker_key)
        ax.scatter(
            x,
            y,
            s=marker_size,
            marker=marker,
            facecolors=new_alpha(to_rgba(color), 0.3),
            edgecolors=color,
            linewidths=float(style["marker_edge_width"]),
            label=series_label,
            zorder=3,
        )

    _add_legend(ax, location, legend_size, ncols, columnspacing)
    ax.tick_params(axis="both", labelsize=tick_size)
    apply_axis_style(ax)

    if fname:
        save(fig, fname, close=False)
    return fig, ax


def plot_errorbar(
    series: List[Tuple],
    location: str = "best",
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    font_size: Optional[float] = None,
    label_size: Optional[float] = None,
    tick_size: Optional[float] = None,
    legend_size: Optional[float] = None,
    capsize: float = 2.5,
    ncols: int = 1,
    columnspacing: float = 0.5,
    grid: Optional[str] = None,
    fname: Optional[str] = "errorbar_plot.pdf",
):
    """Plot line series with error bars."""
    style = get_current_style()
    if fig_size is None:
        fig_size = style["fig_size"]
    _, label_size, tick_size, legend_size = _resolve_text_sizes(
        style, font_size, label_size, tick_size, legend_size
    )

    fig, ax = _prepare_axes(ax, fig_size)
    ax.set_prop_cycle(color=list(style["palette"]))
    ax.set_xlabel(label[0], fontsize=label_size)
    ax.set_ylabel(label[1], fontsize=label_size)
    apply_grid(ax, grid or str(style["line_grid"]))

    for item in series:
        x, y, yerr, color_key, marker_key, series_label = _parse_errorbar_series(item)
        color = resolve_color_key(color_key)
        color_kwargs = {"color": color, "ecolor": color} if color is not None else {}
        marker, marker_size = _resolve_marker(marker_key)
        (line, _, _) = ax.errorbar(
            x,
            y,
            yerr=yerr,
            marker=marker,
            markersize=marker_size * float(style["marker_scale"]),
            markeredgewidth=float(style["marker_edge_width"]),
            linewidth=float(style["line_width"]),
            elinewidth=float(style["line_width"]) * 0.8,
            capsize=capsize,
            label=series_label,
            zorder=3,
            **color_kwargs,
        )
        resolved_color = line.get_color()
        line.set_markerfacecolor(new_alpha(to_rgba(resolved_color), 0.3))
        line.set_markeredgecolor(resolved_color)

    _add_legend(ax, location, legend_size, ncols, columnspacing)
    ax.tick_params(axis="both", labelsize=tick_size)
    apply_axis_style(ax)

    if fname:
        save(fig, fname, close=False)
    return fig, ax


def plot_box(
    groups: List[Tuple],
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("Group", "Value"),
    ax=None,
    font_size: Optional[float] = None,
    label_size: Optional[float] = None,
    tick_size: Optional[float] = None,
    legend_size: Optional[float] = None,
    location: Optional[str] = None,
    grid: Optional[str] = None,
    fname: Optional[str] = "box_plot.pdf",
):
    """Plot grouped distributions as a box plot."""
    style = get_current_style()
    if fig_size is None:
        fig_size = style["fig_size"]
    _, label_size, tick_size, legend_size = _resolve_text_sizes(
        style, font_size, label_size, tick_size, legend_size
    )

    values = []
    labels = []
    colors = []
    palette_iter = cycle(style["palette"])
    for group in groups:
        group_values, color_key, group_label = _parse_box_group(group)
        values.append(group_values)
        labels.append(group_label)
        color = resolve_color_key(color_key)
        colors.append(color if color is not None else next(palette_iter))

    fig, ax = _prepare_axes(ax, fig_size)
    ax.set_xlabel(label[0], fontsize=label_size)
    ax.set_ylabel(label[1], fontsize=label_size)
    apply_grid(ax, grid or "major-y")

    box = ax.boxplot(
        values,
        labels=labels,
        patch_artist=True,
        widths=0.55,
        medianprops=dict(color=str(style["axis_color"])),
    )
    for patch, color in zip(box["boxes"], colors):
        patch.set_facecolor(new_alpha(to_rgba(color), 0.28))
        patch.set_edgecolor(color)
        patch.set_linewidth(float(style["line_width"]))
    for key in ("whiskers", "caps", "medians"):
        for artist in box[key]:
            artist.set_linewidth(float(style["line_width"]))
            artist.set_color(str(style["axis_color"]))

    if location is not None:
        handles = [
            Patch(facecolor=new_alpha(to_rgba(c), 0.28), edgecolor=c) for c in colors
        ]
        legend = ax.legend(
            handles,
            labels,
            loc=location,
            prop=dict(size=legend_size, family=str(style["font_family"])),
            frameon=bool(style["legend_frameon"]),
            framealpha=float(style["legend_framealpha"]),
            facecolor=str(style["legend_face_color"]),
            edgecolor=str(style["legend_edge_color"]),
        )
        apply_legend_style(legend)

    ax.tick_params(axis="both", labelsize=tick_size)
    apply_axis_style(ax)

    if fname:
        save(fig, fname, close=False)
    return fig, ax


def plot_heatmap(
    matrix: Sequence[Sequence[float]],
    fig_size: Optional[Tuple[float, float]] = None,
    label: Tuple[str, str] = ("x-label", "y-label"),
    ax=None,
    xticklabels: Optional[Sequence[str]] = None,
    yticklabels: Optional[Sequence[str]] = None,
    cmap: str = "PuBuGn",
    colorbar_label: Optional[str] = None,
    annotate: bool = False,
    fmt: str = ".2g",
    font_size: Optional[float] = None,
    label_size: Optional[float] = None,
    tick_size: Optional[float] = None,
    legend_size: Optional[float] = None,
    fname: Optional[str] = "heatmap.pdf",
):
    """Plot a matrix heatmap with optional annotations and colorbar."""
    style = get_current_style()
    if fig_size is None:
        fig_size = style["fig_size"]
    _, label_size, tick_size, legend_size = _resolve_text_sizes(
        style, font_size, label_size, tick_size, legend_size
    )

    fig, ax = _prepare_axes(ax, fig_size)
    image = ax.imshow(matrix, cmap=cmap, aspect="auto", zorder=2)
    ax.set_xlabel(label[0], fontsize=label_size)
    ax.set_ylabel(label[1], fontsize=label_size)

    if xticklabels is not None:
        ax.set_xticks(range(len(xticklabels)))
        ax.set_xticklabels(xticklabels, fontsize=tick_size)
    if yticklabels is not None:
        ax.set_yticks(range(len(yticklabels)))
        ax.set_yticklabels(yticklabels, fontsize=tick_size)

    if annotate:
        colormap = plt.get_cmap(cmap)
        for row_idx, row in enumerate(matrix):
            for col_idx, value in enumerate(row):
                cell_color = colormap(image.norm(value))
                luminance = (
                    0.299 * cell_color[0]
                    + 0.587 * cell_color[1]
                    + 0.114 * cell_color[2]
                )
                annotation_color = (
                    "#F5F5F5" if luminance < 0.45 else str(style["text_color"])
                )
                ax.text(
                    col_idx,
                    row_idx,
                    format(value, fmt),
                    ha="center",
                    va="center",
                    fontsize=tick_size,
                    color=annotation_color,
                )

    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.ax.tick_params(labelsize=tick_size, colors=str(style["tick_color"]))
    if colorbar_label is not None:
        colorbar.set_label(
            colorbar_label,
            fontsize=legend_size,
            color=str(style["axis_label_color"]),
        )

    ax.tick_params(axis="both", labelsize=tick_size)
    apply_axis_style(ax)

    if fname:
        save(fig, fname, close=False)
    return fig, ax
