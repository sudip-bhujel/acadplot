# AcadPlot

A simple plotting tool using matplotlib for generating publication-quality plots and subplots for research papers.

> **Note:** Currently, this package only supports line graphs with markers.

## Features

- 📊 Easy-to-use API for creating academic plots
- 🎨 Pre-defined color schemes optimized for academic publications
- 🔷 Multiple marker styles for distinguishing data series
- 📐 LaTeX support for mathematical notation
- 🔧 Customizable plot elements (ticks, grids, legends)
- 📑 Support for both single plots and subplots

## Installation

### From GitHub

```bash
pip install git+https://github.com/sudip-bhujel/acadplot.git
```

or with `uv`:

```bash
uv add git+https://github.com/sudip-bhujel/acadplot.git
```

### Local Installation (Development)

For local development, clone the repository and install in editable mode:

```bash
git clone https://github.com/sudip-bhujel/acadplot.git
cd acadplot
pip install -e .
```

## Requirements

- Python >= 3.14
- matplotlib >= 3.10.8

## Usage

### Basic Plot

```python
from acadplot import plot_line

# Define your data: (x_values, y_values, color, marker, label)
data = [
    ([10, 20, 30, 40, 50], [5, 10, 15, 20, 25], "blue", "x_filled", "Method A"),
    ([10, 20, 30, 40, 50], [6, 11, 14, 18, 22], "orange", "square", "Method B"),
    ([10, 20, 30, 40, 50], [7, 9, 13, 19, 24], "green", "triangle_up", "Method C"),
]

# Create the plot
plot_line(
    data,
    location="upper left",
    label=("X-axis Label", "Y-axis Label"),
    ystart=0,
    yticks=range(0, 30, 5),
    fname="output.pdf"
)
```

### Creating Subplots

```python
import matplotlib.pyplot as plt
from acadplot import plot_line

data = [
    ([10, 20, 30, 40, 50], [5, 10, 15, 20, 25], "blue", "x_filled", "Method A"),
    ([10, 20, 30, 40, 50], [6, 11, 14, 18, 22], "orange", "square", "Method B"),
    ([10, 20, 30, 40, 50], [7, 9, 13, 19, 24], "green", "triangle_up", "Method C"),
]

# Create figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(6, 2))

# Plot on each subplot
plot_line(data, "upper left", ax=axes[0], fname=None)
plot_line(data, "upper right", ax=axes[1], fname=None)

# Adjust layout and save
plt.tight_layout(pad=0.2)
plt.subplots_adjust(wspace=0.27)
plt.savefig("subplots.pdf")
```

### Subplots with Shared Legend

```python
import matplotlib.pyplot as plt
from acadplot import plot_line

data = [
    ([10, 20, 30, 40, 50], [5, 10, 15, 20, 25], "blue", "x_filled", "Method A"),
    ([10, 20, 30, 40, 50], [6, 11, 14, 18, 22], "orange", "square", "Method B"),
    ([10, 20, 30, 40, 50], [7, 9, 13, 19, 24], "green", "triangle_up", "Method C"),
]

fig, axes = plt.subplots(1, 2, figsize=(6, 2))

# Plot on each subplot
plot_line(data, "upper left", ax=axes[0], fname=None)
plot_line(data, "upper right", ax=axes[1], fname=None)

# Remove individual legends
axes[0].get_legend().remove()
axes[1].get_legend().remove()

# Get handles and labels from one subplot
handles, labels = axes[0].get_legend_handles_labels()

# Create a single legend at the bottom center
fig.legend(
    handles,
    labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.1),
    prop=dict(size=6, family="DejaVu Serif"),
    framealpha=0.6,
    columnspacing=0.5,
    ncols=3,
)

plt.tight_layout(pad=0.2)
plt.subplots_adjust(wspace=0.27)
plt.savefig("subplots_shared_legend.pdf", bbox_inches="tight")
```

## Available Colors

Use color names or indices (0-19):

```python
colors = {
    "blue", "orange", "green", "purple", "brown", "yellow",
    "sky_blue", "gray", "red", "pink", "teal", "olive",
    "navy", "maroon", "lime", "cyan", "magenta",
    "dark_gray", "light_gray"
}
```

## Available Markers

Use marker names or indices (0-26):

```python
markers = {
    "square", "triangle_up", "pentagon", "circle", "star",
    "plus_filled", "triangle_down", "diamond", "x_filled",
    "triangle_left", "triangle_right", "thin_diamond",
    "hexagon1", "hexagon2", "plus", "x", "vline", "hline",
    "point", "pixel", "tri_down", "tri_up", "tri_left",
    "tri_right", "octagon", "none"
}
```

## API Reference

### `plot_line(lines, location, label, ax, xticks, yticks, xstart, ystart, font_size, fname)`

**Parameters:
- `lines` (List[Tuple]): List of lines to plot, each defined by `(x_values, y_values, color, marker, label)`
- `location` (str): Location of the legend (e.g., "upper left", "lower right")
- `label` (Tuple[str, str]): Labels for x and y axes. Default: `("x-label", "y-label")`
- `ax` (Optional[plt.Axes]): Axes to plot on. Creates new if None
- `xticks` (Optional[List[float] | range]): Custom x-axis ticks
- `yticks` (Optional[List[float] | range]): Custom y-axis ticks
- `xstart` (Optional[float]): Minimum x-axis value
- `ystart` (Optional[float]): Minimum y-axis value
- `font_size` (int): Font size for the plot. Default: 6
- `fname` (Optional[str]): Filename to save the plot. Default: `"plot.pdf"`

### `draw(ax, x, y, color_key, marker_key, label)`

Draw a single line with markers on the given axes.

### `configure_plot_style()`

Configure global plot style settings with LaTeX rendering.

### Utility Functions

- `kscale(values)`: Convert values to thousands (divide by 1000)
- `new_alpha(color, alpha)`: Create new color with specified alpha
- `blend_color(rgba1, rgba2)`: Blend two RGBA colors

## License

This project is available for use in academic and research projects.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Sudip Bhujel
