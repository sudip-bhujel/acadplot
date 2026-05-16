# Re-export everything from feature modules for backward compatibility
from .bar import plot_bar, plot_grouped_bar, plot_stacked_bar
from .charts import plot_box, plot_errorbar, plot_heatmap, plot_scatter
from .draw import draw, draw_bar
from .line import plot_line
from .styles import (
    available_fonts,
    available_layouts,
    available_themes,
    configure_plot_style,
    get_current_style,
    use_style,
)
from .utils import blend_color, colors, markers, new_alpha, save

__all__ = [
    "plot_line",
    "plot_bar",
    "plot_grouped_bar",
    "plot_stacked_bar",
    "plot_scatter",
    "plot_errorbar",
    "plot_box",
    "plot_heatmap",
    "draw",
    "draw_bar",
    "configure_plot_style",
    "available_fonts",
    "available_layouts",
    "available_themes",
    "get_current_style",
    "use_style",
    "save",
    "colors",
    "markers",
    "new_alpha",
    "blend_color",
]
