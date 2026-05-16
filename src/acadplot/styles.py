from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from typing import Iterator, Literal

import matplotlib.pyplot as plt


GridPreset = Literal["major-y", "major", "major-minor", "none"]


@dataclass(frozen=True)
class LayoutProfile:
    fig_size: tuple[float, float]
    font_size: float
    line_width: float
    marker_scale: float
    marker_edge_width: float
    axes_linewidth: float
    major_tick_width: float
    minor_tick_width: float
    grid_linewidth: float
    minor_grid_linewidth: float
    grid_alpha: float
    minor_grid_alpha: float
    bar_alpha: float
    bar_edge_width: float
    legend_frameon: bool
    legend_framealpha: float
    legend_frame_linewidth: float
    line_grid: GridPreset
    bar_grid: GridPreset


@dataclass(frozen=True)
class Theme:
    colors: dict[str, str]
    palette: tuple[str, ...]
    grid_color: str
    axis_color: str
    axis_label_color: str
    tick_color: str
    legend_text_color: str
    legend_edge_color: str
    legend_face_color: str
    text_color: str


@dataclass(frozen=True)
class FontPreset:
    family: str
    serif: tuple[str, ...]
    sans_serif: tuple[str, ...]
    monospace: tuple[str, ...]
    latex_preamble: str


BASE_COLORS = {
    # Based on Paul Tol's muted qualitative scheme, ordered for line/bar cycles.
    "blue": "#332288",
    "orange": "#DDCC77",
    "green": "#117733",
    "purple": "#AA4499",
    "brown": "#937860",
    "yellow": "#DDCC77",
    "sky_blue": "#88CCEE",
    "gray": "#888888",
    "red": "#CC6677",
    "pink": "#CC6677",
    "teal": "#44AA99",
    "olive": "#999933",
    "navy": "#332288",
    "maroon": "#882255",
    "lime": "#117733",
    "cyan": "#88CCEE",
    "magenta": "#AA4499",
    "dark_gray": "#404040",
    "light_gray": "#D3D3D3",
}


LAYOUTS = {
    "paper-1col": LayoutProfile(
        fig_size=(3.35, 2.1),
        font_size=7.0,
        line_width=0.7,
        marker_scale=0.9,
        marker_edge_width=0.45,
        axes_linewidth=0.5,
        major_tick_width=0.45,
        minor_tick_width=0.3,
        grid_linewidth=0.3,
        minor_grid_linewidth=0.2,
        grid_alpha=0.28,
        minor_grid_alpha=0.14,
        bar_alpha=0.86,
        bar_edge_width=0.25,
        legend_frameon=True,
        legend_framealpha=0.6,
        legend_frame_linewidth=0.2,
        line_grid="major",
        bar_grid="major-y",
    ),
    "paper-2col": LayoutProfile(
        fig_size=(6.8, 2.8),
        font_size=8.0,
        line_width=0.9,
        marker_scale=1.05,
        marker_edge_width=0.55,
        axes_linewidth=0.55,
        major_tick_width=0.5,
        minor_tick_width=0.35,
        grid_linewidth=0.35,
        minor_grid_linewidth=0.22,
        grid_alpha=0.26,
        minor_grid_alpha=0.12,
        bar_alpha=0.88,
        bar_edge_width=0.3,
        legend_frameon=True,
        legend_framealpha=0.6,
        legend_frame_linewidth=0.2,
        line_grid="major",
        bar_grid="major-y",
    ),
    "presentation": LayoutProfile(
        fig_size=(7.2, 4.2),
        font_size=12.0,
        line_width=1.4,
        marker_scale=1.45,
        marker_edge_width=0.8,
        axes_linewidth=0.8,
        major_tick_width=0.75,
        minor_tick_width=0.45,
        grid_linewidth=0.5,
        minor_grid_linewidth=0.3,
        grid_alpha=0.24,
        minor_grid_alpha=0.12,
        bar_alpha=0.9,
        bar_edge_width=0.45,
        legend_frameon=True,
        legend_framealpha=0.65,
        legend_frame_linewidth=0.25,
        line_grid="major",
        bar_grid="major-y",
    ),
}


THEMES = {
    "classic": Theme(
        colors=BASE_COLORS,
        palette=(
            "#332288",
            "#DDCC77",
            "#117733",
            "#CC6677",
            "#88CCEE",
            "#882255",
            "#44AA99",
            "#999933",
            "#AA4499",
            "#888888",
        ),
        grid_color="#A9A9A9",
        axis_color="#3A3A3A",
        axis_label_color="#3F3F3F",
        tick_color="#3F3F3F",
        legend_text_color="#3F3F3F",
        legend_edge_color="#DADADA",
        legend_face_color="#FFFFFF",
        text_color="#3F3F3F",
    ),
    "nature": Theme(
        colors={
            "blue": "#6A408D",
            "orange": "#77B5B6",
            "green": "#7E7E7E",
            "purple": "#9671BD",
            "brown": "#A67C52",
            "yellow": "#DDAA33",
            "sky_blue": "#A6D5D6",
            "gray": "#8A8A8A",
            "red": "#B35850",
            "pink": "#C9A3D8",
            "teal": "#378D94",
            "olive": "#7B8D42",
            "navy": "#50336F",
            "maroon": "#7A3B46",
            "lime": "#8DB67B",
            "cyan": "#9FD8DA",
            "magenta": "#B681C4",
            "dark_gray": "#4E4E4E",
            "light_gray": "#D9D9D9",
        },
        palette=("#9671BD", "#77B5B6", "#7E7E7E", "#6A408D", "#378D94"),
        grid_color="#A5A5A5",
        axis_color="#3A3A3A",
        axis_label_color="#3F3F3F",
        tick_color="#3F3F3F",
        legend_text_color="#3F3F3F",
        legend_edge_color="#D8D8D8",
        legend_face_color="#FFFFFF",
        text_color="#3F3F3F",
    ),
    "colorblind": Theme(
        colors={
            "blue": "#0072B2",
            "orange": "#E69F00",
            "green": "#009E73",
            "purple": "#CC79A7",
            "brown": "#A6761D",
            "yellow": "#F0E442",
            "sky_blue": "#56B4E9",
            "gray": "#8F8F8F",
            "red": "#D55E00",
            "pink": "#CC79A7",
            "teal": "#009E73",
            "olive": "#7F8C3A",
            "navy": "#0072B2",
            "maroon": "#8C3A3A",
            "lime": "#7FBF7B",
            "cyan": "#56B4E9",
            "magenta": "#CC79A7",
            "dark_gray": "#3F3F3F",
            "light_gray": "#D4D4D4",
        },
        palette=(
            "#0072B2",
            "#E69F00",
            "#009E73",
            "#CC79A7",
            "#D55E00",
            "#56B4E9",
            "#F0E442",
            "#000000",
        ),
        grid_color="#A8A8A8",
        axis_color="#3A3A3A",
        axis_label_color="#3F3F3F",
        tick_color="#3F3F3F",
        legend_text_color="#3F3F3F",
        legend_edge_color="#DADADA",
        legend_face_color="#FFFFFF",
        text_color="#3F3F3F",
    ),
    "mono": Theme(
        colors={
            "blue": "#111111",
            "orange": "#333333",
            "green": "#555555",
            "purple": "#777777",
            "brown": "#999999",
            "yellow": "#BBBBBB",
            "sky_blue": "#666666",
            "gray": "#8C8C8C",
            "red": "#222222",
            "pink": "#AAAAAA",
            "teal": "#444444",
            "olive": "#606060",
            "navy": "#181818",
            "maroon": "#383838",
            "lime": "#B0B0B0",
            "cyan": "#707070",
            "magenta": "#909090",
            "dark_gray": "#303030",
            "light_gray": "#D0D0D0",
        },
        palette=("#111111", "#333333", "#555555", "#777777", "#999999"),
        grid_color="#B0B0B0",
        axis_color="#3A3A3A",
        axis_label_color="#3F3F3F",
        tick_color="#3F3F3F",
        legend_text_color="#3F3F3F",
        legend_edge_color="#D4D4D4",
        legend_face_color="#FFFFFF",
        text_color="#3F3F3F",
    ),
    "warm": Theme(
        colors={
            "blue": "#3A6EA5",
            "orange": "#C8792A",
            "green": "#6E8B3D",
            "purple": "#875A7B",
            "brown": "#8B5E3C",
            "yellow": "#D6A84F",
            "sky_blue": "#6B9AC4",
            "gray": "#8A837C",
            "red": "#B55239",
            "pink": "#B76E79",
            "teal": "#5F8A8B",
            "olive": "#827B3D",
            "navy": "#304E6E",
            "maroon": "#7B3F36",
            "lime": "#A6B46A",
            "cyan": "#7AA6A6",
            "magenta": "#A05D83",
            "dark_gray": "#4C4742",
            "light_gray": "#D8D0C8",
        },
        palette=("#B55239", "#C8792A", "#D6A84F", "#6E8B3D", "#3A6EA5"),
        grid_color="#B5ACA3",
        axis_color="#443E39",
        axis_label_color="#4A4540",
        tick_color="#4A4540",
        legend_text_color="#4A4540",
        legend_edge_color="#D9D0C8",
        legend_face_color="#FFFFFF",
        text_color="#4A4540",
    ),
}


FONTS = {
    "libertine": FontPreset(
        family="serif",
        serif=("Linux Libertine O", "Libertinus Serif", "Libertine", "DejaVu Serif"),
        sans_serif=("DejaVu Sans",),
        monospace=("DejaVu Sans Mono", "Courier New", "Courier"),
        latex_preamble=r"\usepackage{libertine}\usepackage[libertine]{newtxmath}",
    ),
    "inconsolata": FontPreset(
        family="monospace",
        serif=("DejaVu Serif",),
        sans_serif=("DejaVu Sans",),
        monospace=("Inconsolata", "DejaVu Sans Mono", "Courier New", "Courier"),
        latex_preamble=r"\usepackage[varqu]{zi4}",
    ),
    "serif": FontPreset(
        family="serif",
        serif=("DejaVu Serif", "Times New Roman", "Times"),
        sans_serif=("DejaVu Sans",),
        monospace=("DejaVu Sans Mono", "Courier New", "Courier"),
        latex_preamble="",
    ),
    "sans": FontPreset(
        family="sans-serif",
        serif=("DejaVu Serif",),
        sans_serif=("DejaVu Sans", "Arial", "Helvetica"),
        monospace=("DejaVu Sans Mono", "Courier New", "Courier"),
        latex_preamble=r"\usepackage{sansmath}",
    ),
}


_VALID_GRIDS = {"major-y", "major", "major-minor", "none"}


def _build_style(
    layout: str,
    theme: str,
    font: str,
    latex: bool,
) -> dict[str, object]:
    if layout not in LAYOUTS:
        raise ValueError(
            f"Unknown layout {layout!r}. Choose from: {', '.join(available_layouts())}."
        )
    if theme not in THEMES:
        raise ValueError(
            f"Unknown theme {theme!r}. Choose from: {', '.join(available_themes())}."
        )
    if font not in FONTS:
        raise ValueError(f"Unknown font {font!r}. Choose from: {', '.join(FONTS)}.")

    layout_profile = LAYOUTS[layout]
    theme_profile = THEMES[theme]
    font_profile = FONTS[font]

    return {
        "layout": layout,
        "theme": theme,
        "font": font,
        "latex": latex,
        "fig_size": layout_profile.fig_size,
        "font_size": layout_profile.font_size,
        "font_family": font_profile.family,
        "line_width": layout_profile.line_width,
        "marker_scale": layout_profile.marker_scale,
        "marker_edge_width": layout_profile.marker_edge_width,
        "axes_linewidth": layout_profile.axes_linewidth,
        "major_tick_width": layout_profile.major_tick_width,
        "minor_tick_width": layout_profile.minor_tick_width,
        "grid_color": theme_profile.grid_color,
        "grid_linewidth": layout_profile.grid_linewidth,
        "minor_grid_linewidth": layout_profile.minor_grid_linewidth,
        "grid_alpha": layout_profile.grid_alpha,
        "minor_grid_alpha": layout_profile.minor_grid_alpha,
        "bar_alpha": layout_profile.bar_alpha,
        "bar_edge_width": layout_profile.bar_edge_width,
        "legend_frameon": layout_profile.legend_frameon,
        "legend_framealpha": layout_profile.legend_framealpha,
        "legend_frame_linewidth": layout_profile.legend_frame_linewidth,
        "line_grid": layout_profile.line_grid,
        "bar_grid": layout_profile.bar_grid,
        "colors": deepcopy(theme_profile.colors),
        "palette": theme_profile.palette,
        "axis_color": theme_profile.axis_color,
        "axis_label_color": theme_profile.axis_label_color,
        "tick_color": theme_profile.tick_color,
        "legend_text_color": theme_profile.legend_text_color,
        "legend_edge_color": theme_profile.legend_edge_color,
        "legend_face_color": theme_profile.legend_face_color,
        "text_color": theme_profile.text_color,
    }


_CURRENT_STYLE = _build_style("paper-1col", "classic", "libertine", True)


def available_layouts() -> tuple[str, ...]:
    """Return the names of available publication layout profiles."""
    return tuple(LAYOUTS)


def available_themes() -> tuple[str, ...]:
    """Return the names of available professional visual themes."""
    return tuple(THEMES)


def get_current_style() -> dict[str, object]:
    """Return a copy of the active AcadPlot style settings."""
    return deepcopy(_CURRENT_STYLE)


def _sync_public_colors(style: dict[str, object]) -> None:
    from . import utils

    utils.colors.clear()
    utils.colors.update(style["colors"])


def _apply_rcparams(style: dict[str, object]) -> None:
    font = FONTS[str(style["font"])]
    text_color = str(style["text_color"])
    axis_color = str(style["axis_color"])
    axis_label_color = str(style["axis_label_color"])
    tick_color = str(style["tick_color"])

    plt.rcParams.update(
        {
            "text.usetex": bool(style["latex"]),
            "font.family": font.family,
            "font.serif": list(font.serif),
            "font.sans-serif": list(font.sans_serif),
            "font.monospace": list(font.monospace),
            "font.size": float(style["font_size"]),
            "axes.linewidth": float(style["axes_linewidth"]),
            "axes.labelsize": float(style["font_size"]),
            "axes.labelcolor": axis_label_color,
            "axes.edgecolor": axis_color,
            "axes.prop_cycle": plt.cycler(color=list(style["palette"])),
            "xtick.labelsize": float(style["font_size"]),
            "ytick.labelsize": float(style["font_size"]),
            "xtick.color": tick_color,
            "ytick.color": tick_color,
            "xtick.major.width": float(style["major_tick_width"]),
            "ytick.major.width": float(style["major_tick_width"]),
            "xtick.minor.width": float(style["minor_tick_width"]),
            "ytick.minor.width": float(style["minor_tick_width"]),
            "legend.fontsize": float(style["font_size"]),
            "legend.labelcolor": str(style["legend_text_color"]),
            "legend.facecolor": str(style["legend_face_color"]),
            "legend.edgecolor": str(style["legend_edge_color"]),
            "legend.frameon": bool(style["legend_frameon"]),
            "legend.framealpha": float(style["legend_framealpha"]),
            "figure.figsize": tuple(style["fig_size"]),
            "grid.color": str(style["grid_color"]),
            "grid.linewidth": float(style["grid_linewidth"]),
            "grid.alpha": float(style["grid_alpha"]),
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "savefig.dpi": 300,
        }
    )

    if bool(style["latex"]):
        plt.rcParams["text.latex.preamble"] = font.latex_preamble
    else:
        plt.rcParams["text.latex.preamble"] = ""


def configure_plot_style(
    layout: str = "paper-1col",
    theme: str = "classic",
    font: str = "libertine",
    latex: bool = True,
) -> dict[str, object]:
    """
    Configure global AcadPlot style settings.

    Declare this once near the top of a script to set publication layout,
    theme colours, font family, and Matplotlib rendering defaults.
    """
    global _CURRENT_STYLE

    _CURRENT_STYLE = _build_style(layout, theme, font, latex)
    _apply_rcparams(_CURRENT_STYLE)
    _sync_public_colors(_CURRENT_STYLE)
    return get_current_style()


@contextmanager
def use_style(
    layout: str | None = None,
    theme: str | None = None,
    font: str | None = None,
    latex: bool | None = None,
) -> Iterator[dict[str, object]]:
    """Temporarily apply an AcadPlot style inside a ``with`` block."""
    global _CURRENT_STYLE

    previous_style = get_current_style()
    previous_rcparams = plt.rcParams.copy()

    try:
        yield configure_plot_style(
            layout=layout or str(previous_style["layout"]),
            theme=theme or str(previous_style["theme"]),
            font=font or str(previous_style["font"]),
            latex=bool(previous_style["latex"]) if latex is None else latex,
        )
    finally:
        _CURRENT_STYLE = previous_style
        plt.rcParams.update(previous_rcparams)
        _sync_public_colors(_CURRENT_STYLE)


def apply_axis_style(ax) -> None:
    """Apply theme axis, tick, and label colors to an axes."""
    style = get_current_style()
    axis_color = str(style["axis_color"])
    axis_label_color = str(style["axis_label_color"])
    tick_color = str(style["tick_color"])

    ax.xaxis.label.set_color(axis_label_color)
    ax.yaxis.label.set_color(axis_label_color)
    ax.tick_params(axis="both", colors=tick_color)
    for spine in ax.spines.values():
        spine.set_color(axis_color)


def apply_legend_style(legend) -> None:
    """Apply theme legend text and frame colors."""
    style = get_current_style()
    for text in legend.get_texts():
        text.set_color(str(style["legend_text_color"]))

    frame = legend.get_frame()
    frame.set_facecolor(str(style["legend_face_color"]))
    frame.set_edgecolor(str(style["legend_edge_color"]))
    frame.set_alpha(float(style["legend_framealpha"]))
    frame.set_linewidth(float(style["legend_frame_linewidth"]))


def apply_grid(ax, grid: str) -> None:
    """Apply one of AcadPlot's supported grid presets to an axes."""
    if grid not in _VALID_GRIDS:
        raise ValueError(
            f"Unknown grid {grid!r}. Choose from: {', '.join(_VALID_GRIDS)}."
        )

    style = get_current_style()
    ax.grid(False, which="both", axis="both")
    ax.set_axisbelow(True)

    if grid == "none":
        return

    common = {
        "color": str(style["grid_color"]),
        "linestyle": "-",
        "linewidth": float(style["grid_linewidth"]),
        "alpha": float(style["grid_alpha"]),
    }

    if grid == "major-y":
        ax.grid(True, which="major", axis="y", **common)
        return

    ax.grid(True, which="major", axis="both", **common)

    if grid == "major-minor":
        ax.minorticks_on()
        ax.grid(
            True,
            which="minor",
            axis="both",
            color=str(style["grid_color"]),
            linestyle="-",
            linewidth=float(style["minor_grid_linewidth"]),
            alpha=float(style["minor_grid_alpha"]),
        )
