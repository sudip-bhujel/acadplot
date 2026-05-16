from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from acadplot import (  # noqa: E402
    configure_plot_style,
    plot_bar,
    plot_grouped_bar,
    plot_line,
    plot_stacked_bar,
)

OUT = Path(__file__).resolve().parent


LINE_DATA = [
    ([1, 2, 3, 4, 5], [76.0, 79.5, 82.0, 83.0, 84.0], "circle", "Method A"),
    ([1, 2, 3, 4, 5], [74.0, 77.0, 79.0, 80.5, 81.5], "square", "Method B"),
    ([1, 2, 3, 4, 5], [72.0, 74.5, 77.5, 78.5, 80.0], "triangle_up", "Method C"),
]


def save(fig, name: str, *, pdf: bool = False) -> None:
    fig.savefig(OUT / f"{name}.png", dpi=300, bbox_inches="tight", pad_inches=0)
    if pdf:
        fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", pad_inches=0)
    plt.close(fig)


def generate_line_example() -> None:
    configure_plot_style(
        layout="paper-1col", theme="classic", latex=True
    )
    fig, _ = plot_line(
        LINE_DATA,
        location="lower right",
        label=("Training budget", r"Accuracy (\%)"),
        xticks=[1, 2, 3, 4, 5],
        yticks=range(72, 87, 2),
        ystart=71,
        fname=None,
    )
    save(fig, "plot", pdf=True)


def generate_subplot_example() -> None:
    configure_plot_style(
        layout="paper-2col-span", theme="colorblind", latex=True
    )
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.5), sharey=True)
    plot_line(
        LINE_DATA[:2],
        "lower right",
        ax=axes[0],
        label=("Budget", r"Accuracy (\%)"),
        xticks=[1, 2, 3, 4, 5],
        yticks=range(72, 87, 2),
        fname=None,
    )
    plot_line(
        LINE_DATA[1:],
        "lower right",
        ax=axes[1],
        label=("Budget", r"Accuracy (\%)"),
        xticks=[1, 2, 3, 4, 5],
        yticks=range(72, 87, 2),
        fname=None,
    )
    axes[0].set_title("Small data regime")
    axes[1].set_title("Large data regime")
    fig.tight_layout(pad=0.3, w_pad=1.5)
    save(fig, "subplot", pdf=True)


def generate_bar_examples() -> None:
    configure_plot_style(
        layout="paper-1col", theme="nature", latex=True
    )
    fig, _ = plot_bar(
        [
            ([0, 1, 2], [81.2, 84.4, 86.1], "Baseline"),
            ([0, 1, 2], [83.5, 86.2, 88.0], "AcadPlot"),
        ],
        location="upper left",
        label=("Dataset", "Score"),
        xticklabels=["A", "B", "C"],
        fname=None,
    )
    save(fig, "bar_plot")

    configure_plot_style(
        layout="paper-2col", theme="colorblind", latex=True
    )
    fig, _ = plot_grouped_bar(
        [
            ("Dataset A", [(81.2, "Baseline"), (83.5, "AcadPlot")]),
            ("Dataset B", [(84.4, "Baseline"), (86.2, "AcadPlot")]),
            ("Dataset C", [(86.1, "Baseline"), (88.0, "AcadPlot")]),
        ],
        location="upper left",
        label=("Dataset", "Score"),
        fname=None,
    )
    save(fig, "grouped_bar_plot")

    configure_plot_style(
        layout="paper-1col", theme="mono", latex=True
    )
    fig, _ = plot_stacked_bar(
        ["Ablation 1", "Ablation 2", "Ablation 3"],
        [
            ([35, 42, 38], "Compute"),
            ([25, 22, 30], "Memory"),
            ([18, 16, 20], "I/O"),
        ],
        location="upper left",
        label=("Experiment", "Runtime share"),
        rotation=8,
        fname=None,
    )
    save(fig, "stacked_bar_plot")


def generate_presentation_example() -> None:
    configure_plot_style(
        layout="presentation", theme="warm", latex=True
    )
    fig, _ = plot_line(
        [
            ([0, 1, 2, 3, 4], [54, 61, 67, 73, 79], "circle", "Model"),
            ([0, 1, 2, 3, 4], [50, 55, 60, 64, 67], "square", "Reference"),
        ],
        location="upper left",
        label=("Iteration", "Quality score"),
        xticks=[0, 1, 2, 3, 4],
        yticks=range(50, 85, 5),
        grid="major-minor",
        fname=None,
    )
    save(fig, "presentation_style")


def generate_monospace_example() -> None:
    configure_plot_style(
        layout="paper-2col", theme="classic", latex=True
    )
    fig, _ = plot_line(
        [
            ([1, 2, 3, 4, 5], [0.42, 0.55, 0.63, 0.68, 0.71], "circle", "Model"),
            ([1, 2, 3, 4, 5], [0.38, 0.47, 0.54, 0.59, 0.62], "square", "Baseline"),
        ],
        location="lower right",
        label=("Epoch", "Calibration error"),
        xticks=[1, 2, 3, 4, 5],
        yticks=[0.35, 0.45, 0.55, 0.65, 0.75],
        grid="major",
        fname=None,
    )
    save(fig, "monospace_style", pdf=True)


def generate_style_gallery() -> None:
    themes = ["classic", "nature", "colorblind", "mono", "warm"]
    fig, axes = plt.subplots(
        len(themes), 1, figsize=(6.8, 7.2), sharex=True, sharey=True
    )

    for ax, theme in zip(axes, themes):
        configure_plot_style(
            layout="paper-2col-span", theme=theme, latex=True
        )
        plot_line(
            LINE_DATA,
            "lower right",
            ax=ax,
            label=("Budget", r"Accuracy (\%)"),
            xticks=[1, 2, 3, 4, 5],
            yticks=range(72, 87, 4),
            fname=None,
        )
        ax.set_title(theme)

    fig.tight_layout(pad=0.4, h_pad=0.9)
    save(fig, "style_gallery")


def main() -> None:
    generate_line_example()
    generate_subplot_example()
    generate_bar_examples()
    generate_presentation_example()
    generate_monospace_example()
    generate_style_gallery()


if __name__ == "__main__":
    main()
