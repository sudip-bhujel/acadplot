from pathlib import Path
from datetime import datetime, timezone
import json
from typing import Iterable, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


_OUTPUT_DIR: Path | None = None


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


def _normalize_formats(formats: Iterable[str]) -> tuple[str, ...]:
    normalized = []
    for fmt in formats:
        clean = fmt.lower().lstrip(".")
        if clean and clean not in normalized:
            normalized.append(clean)
    return tuple(normalized)


def set_output_dir(directory: str | Path | None) -> Path | None:
    """Set the default directory used by ``save`` for relative output names."""
    global _OUTPUT_DIR

    _OUTPUT_DIR = None if directory is None else Path(directory)
    return _OUTPUT_DIR


def get_output_dir() -> Path | None:
    """Return the default output directory used by ``save``."""
    return _OUTPUT_DIR


def _resolve_output_path(name: str | Path, directory: str | Path | None) -> Path:
    path = Path(name)
    output_dir = Path(directory) if directory is not None else _OUTPUT_DIR
    if output_dir is not None and not path.is_absolute():
        path = output_dir / path
    return path


def _write_save_metadata(
    targets: tuple[Path, ...],
    metadata: bool | str | Path,
) -> Path:
    from matplotlib import __version__ as matplotlib_version

    from .styles import get_current_style

    metadata_path = (
        targets[0].with_suffix(".acadplot.json")
        if metadata is True
        else Path(metadata)
    )
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "outputs": [str(target) for target in targets],
        "matplotlib_version": matplotlib_version,
        "style": get_current_style(),
    }
    metadata_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return metadata_path


def save(
    fig,
    name: str | Path,
    *,
    directory: str | Path | None = None,
    formats: Iterable[str] | None = None,
    png: bool = True,
    pdf: bool = False,
    svg: bool = False,
    dpi: int | float = 300,
    bbox_inches: str | None = "tight",
    pad_inches: float = 0,
    tight_layout: bool = True,
    tight_pad: float = 0.2,
    close: bool = True,
    transparent: bool = False,
    metadata: bool | str | Path = False,
    **savefig_kwargs,
) -> tuple[Path, ...]:
    """Save a figure with publication-oriented defaults.

    If ``name`` has a file extension, that exact file is written. Otherwise the
    requested formats are appended to ``name``. By default AcadPlot writes PNG
    output and uses a tight bounding box with no padding.
    """
    path = _resolve_output_path(name, directory)

    if path.suffix:
        targets = (path,)
    else:
        selected_formats = []
        if formats is None:
            if png:
                selected_formats.append("png")
            if pdf:
                selected_formats.append("pdf")
            if svg:
                selected_formats.append("svg")
        else:
            selected_formats.extend(formats)
            if pdf:
                selected_formats.append("pdf")
            if svg:
                selected_formats.append("svg")

        normalized_formats = _normalize_formats(selected_formats)
        if not normalized_formats:
            raise ValueError("At least one output format must be requested.")
        targets = tuple(path.with_suffix(f".{fmt}") for fmt in normalized_formats)

    if tight_layout:
        fig.tight_layout(pad=tight_pad)

    for target in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(
            target,
            dpi=dpi,
            bbox_inches=bbox_inches,
            pad_inches=pad_inches,
            transparent=transparent,
            **savefig_kwargs,
        )

    if close:
        plt.close(fig)

    if metadata:
        _write_save_metadata(targets, metadata)

    return targets


def save_all(
    fig,
    name: str | Path,
    *,
    formats: Iterable[str] = ("png", "pdf", "svg"),
    **kwargs,
) -> tuple[Path, ...]:
    """Save PNG, PDF, and SVG outputs unless a different format set is given."""
    return save(fig, name, formats=formats, **kwargs)


def _legend_location(location: str, legend_outside: bool | str) -> dict[str, object]:
    if not legend_outside:
        return {"loc": location}

    side = "right" if legend_outside is True else str(legend_outside).lower()
    outside_locations = {
        "right": {"loc": "center left", "bbox_to_anchor": (1.02, 0.5)},
        "left": {"loc": "center right", "bbox_to_anchor": (-0.02, 0.5)},
        "top": {"loc": "lower center", "bbox_to_anchor": (0.5, 1.02)},
        "bottom": {"loc": "upper center", "bbox_to_anchor": (0.5, -0.18)},
    }
    if side not in outside_locations:
        raise ValueError("legend_outside must be True, False, or one of: right, left, top, bottom.")
    return outside_locations[side]


def styled_legend(
    ax,
    location: str = "best",
    *,
    legend_size: float | None = None,
    ncols: int = 1,
    columnspacing: float = 0.5,
    legend_outside: bool | str = False,
    handles=None,
    labels=None,
):
    """Create a legend using the active AcadPlot style."""
    from .styles import apply_legend_style, get_current_style

    style = get_current_style()
    kwargs = _legend_location(location, legend_outside)
    legend = ax.legend(
        handles=handles,
        labels=labels,
        prop=dict(
            size=float(style["legend_size"]) if legend_size is None else legend_size,
            family=str(style["font_family"]),
        ),
        frameon=bool(style["legend_frameon"]),
        framealpha=float(style["legend_framealpha"]),
        facecolor=str(style["legend_face_color"]),
        edgecolor=str(style["legend_edge_color"]),
        ncols=ncols,
        columnspacing=columnspacing,
        **kwargs,
    )
    apply_legend_style(legend)
    return legend


def format_legend(legend=None):
    """Apply AcadPlot styling to an existing Matplotlib legend."""
    from .styles import apply_legend_style

    if legend is None:
        legend = plt.gca().get_legend()
    if legend is None:
        return None
    apply_legend_style(legend)
    return legend


def panel_labels(
    axes,
    labels: Sequence[str] | None = None,
    *,
    x: float = -0.08,
    y: float = 1.04,
    font_size: float | None = None,
    weight: str = "bold",
    prefix: str = "(",
    suffix: str = ")",
):
    """Add panel labels such as ``(a)``, ``(b)``, and ``(c)`` to axes."""
    from .styles import get_current_style

    flat_axes = _flatten_axes(axes)
    style = get_current_style()
    if labels is None:
        labels = [chr(ord("a") + idx) for idx in range(len(flat_axes))]
    if len(labels) != len(flat_axes):
        raise ValueError("labels must match the number of axes.")

    text_objects = []
    for ax, label in zip(flat_axes, labels):
        text_objects.append(
            ax.text(
                x,
                y,
                f"{prefix}{label}{suffix}",
                transform=ax.transAxes,
                ha="left",
                va="bottom",
                fontsize=float(style["label_size"]) if font_size is None else font_size,
                fontweight=weight,
                color=str(style["text_color"]),
                family=str(style["font_family"]),
            )
        )
    return text_objects


def annotate_points(
    ax,
    points: Sequence[tuple[float, float, str]],
    *,
    xytext: tuple[float, float] = (4, 4),
    font_size: float | None = None,
    arrow: bool = False,
    **kwargs,
):
    """Annotate selected points using active AcadPlot text styling."""
    from .styles import get_current_style

    style = get_current_style()
    annotations = []
    arrowprops = (
        {"arrowstyle": "-", "color": str(style["axis_color"]), "linewidth": 0.5}
        if arrow
        else None
    )
    for x, y, text in points:
        annotations.append(
            ax.annotate(
                text,
                xy=(x, y),
                xytext=xytext,
                textcoords="offset points",
                fontsize=float(style["tick_size"]) if font_size is None else font_size,
                color=str(style["text_color"]),
                family=str(style["font_family"]),
                arrowprops=arrowprops,
                **kwargs,
            )
        )
    return annotations


def theme_preview(
    *,
    layout: str | None = None,
    themes: Sequence[str] | None = None,
    fig_size: tuple[float, float] | None = None,
):
    """Create a compact preview figure for AcadPlot theme palettes."""
    from .styles import THEMES, figure_size, format_axes, get_current_style

    selected_themes = list(THEMES if themes is None else themes)
    for theme in selected_themes:
        if theme not in THEMES:
            raise ValueError(f"Unknown theme {theme!r}.")

    if fig_size is None:
        base_width, _ = figure_size(layout)
        fig_size = (base_width, max(1.0, 0.36 * len(selected_themes)))
    fig, ax = plt.subplots(figsize=fig_size)

    for row_idx, theme_name in enumerate(selected_themes):
        palette = THEMES[theme_name].palette
        ax.text(
            -0.25,
            row_idx + 0.5,
            theme_name,
            ha="right",
            va="center",
            fontsize=float(get_current_style()["tick_size"]),
            color=str(get_current_style()["text_color"]),
        )
        for col_idx, color in enumerate(palette):
            ax.add_patch(
                Rectangle((col_idx, row_idx), 0.9, 0.72, facecolor=color, edgecolor="none")
            )

    ax.set_xlim(-1.2, max(len(THEMES[name].palette) for name in selected_themes))
    ax.set_ylim(0, len(selected_themes))
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.set_yticks([])
    format_axes(ax, grid="none", despine=True)
    return fig, ax


def _flatten_axes(axes) -> list:
    if hasattr(axes, "ravel"):
        return list(axes.ravel())
    if isinstance(axes, (list, tuple)):
        flat = []
        for item in axes:
            flat.extend(_flatten_axes(item))
        return flat
    return [axes]


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
    "heart": (r"$\heartsuit$", 4),
    "club": (r"$\clubsuit$", 4),
    "spade": (r"$\spadesuit$", 4),
    "diamond_suit": (r"$\diamondsuit$", 4),
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
