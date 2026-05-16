# Re-export everything from feature modules for backward compatibility
from .bar import plot_bar, plot_grouped_bar, plot_stacked_bar
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
from .utils import blend_color, colors, markers, new_alpha

__all__ = [
    "plot_line",
    "plot_bar",
    "plot_grouped_bar",
    "plot_stacked_bar",
    "draw",
    "draw_bar",
    "configure_plot_style",
    "available_fonts",
    "available_layouts",
    "available_themes",
    "get_current_style",
    "use_style",
    "colors",
    "markers",
    "new_alpha",
    "blend_color",
]
