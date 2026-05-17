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
    annotate_points,
    configure_plot_style,
    figure_size,
    format_axes,
    format_legend,
    panel_labels,
    plot_bar,
    plot_box,
    plot_errorbar,
    plot_grouped_bar,
    plot_heatmap,
    plot_line,
    plot_scatter,
    plot_stacked_bar,
    save,
)

OUT = Path(__file__).resolve().parent


LINE_DATA = [
    ([1, 2, 3, 4, 5], [76.0, 79.5, 82.0, 83.0, 84.0], "circle", "Method A"),
    ([1, 2, 3, 4, 5], [74.0, 77.0, 79.0, 80.5, 81.5], "square", "Method B"),
    ([1, 2, 3, 4, 5], [72.0, 74.5, 77.5, 78.5, 80.0], "triangle_up", "Method C"),
]


def save_example(
    fig, name: str, *, pdf: bool = False, tight_layout: bool = True
) -> None:
    save(fig, name, directory=OUT, pdf=pdf, tight_layout=tight_layout)


def generate_line_example() -> None:
    configure_plot_style(layout="paper-1col", theme="classic", latex=True)
    fig, _ = plot_line(
        LINE_DATA,
        location="lower right",
        label=("Training budget", r"Accuracy (\%)"),
        xticks=[1, 2, 3, 4, 5],
        yticks=range(72, 87, 2),
        ystart=71,
        fname=None,
    )
    save_example(fig, "plot", pdf=True)


def generate_subplot_example() -> None:
    configure_plot_style(layout="paper-2col-subplot", theme="colorblind", latex=True)
    fig, axes = plt.subplots(
        1,
        2,
        figsize=figure_size(),
        sharey=True,
        gridspec_kw={"wspace": 0.1},
    )
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
    axes[1].set_ylabel("")
    axes[1].tick_params(axis="y", left=False)
    fig.subplots_adjust(left=0.14, right=0.99, bottom=0.24, top=0.86, wspace=0.18)
    save_example(fig, "subplot", pdf=True, tight_layout=False)


def generate_bar_examples() -> None:
    configure_plot_style(layout="paper-1col", theme="nature", latex=True)
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
    save_example(fig, "bar_plot")

    configure_plot_style(layout="paper-2col", theme="colorblind", latex=True)
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
    save_example(fig, "grouped_bar_plot")

    configure_plot_style(layout="paper-1col", theme="mono", latex=True)
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
    save_example(fig, "stacked_bar_plot")


def generate_presentation_example() -> None:
    configure_plot_style(layout="presentation", theme="warm", latex=True)
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
    save_example(fig, "presentation_style")


def generate_monospace_example() -> None:
    configure_plot_style(layout="paper-2col", theme="classic", latex=True)
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
    save_example(fig, "monospace_style", pdf=True)


def generate_top_legend_example() -> None:
    configure_plot_style(
        layout="paper-2col", theme="classic", latex=True, legend_size=8.5
    )
    fig, _ = plot_line(
        LINE_DATA,
        location="lower center",
        label=("Training budget", r"Accuracy (\%)"),
        xticks=[1, 2, 3, 4, 5],
        yticks=range(72, 87, 2),
        ystart=71,
        ncols=3,
        columnspacing=0.9,
        legend_outside="top",
        fname=None,
    )
    save_example(fig, "top_legend_plot")


def generate_text_color_example() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(6.8, 1.85), sharey=True)
    presets = [
        ("dark", "Preset: dark"),
        ("gray", "Preset: gray"),
        ("#202020", "Custom hex"),
    ]

    for ax, (text_color, title) in zip(axes, presets):
        configure_plot_style(
            layout="paper-2col-span",
            theme="classic",
            latex=True,
            text_color=text_color,
            tick_size=6.5,
            label_size=7.0,
            legend_size=6.5,
            title_size=7.0,
        )
        plot_line(
            LINE_DATA[:2],
            "lower right",
            ax=ax,
            label=("Budget", r"Accuracy (\%)"),
            xticks=[1, 2, 3, 4, 5],
            yticks=range(74, 86, 4),
            grid="major-y",
            fname=None,
        )
        ax.set_title(title)
        if ax is not axes[0]:
            ax.set_ylabel("")
            ax.tick_params(axis="y", left=False)

    fig.subplots_adjust(left=0.08, right=0.99, bottom=0.24, top=0.82, wspace=0.18)
    save_example(fig, "text_color_styles", tight_layout=False)


def generate_scatter_example() -> None:
    configure_plot_style(layout="paper-2col", theme="classic", latex=True)
    fig, _ = plot_scatter(
        [
            (
                [1.0, 1.4, 1.8, 2.2, 2.6],
                [0.42, 0.45, 0.49, 0.53, 0.58],
                "circle",
                "Lab A",
            ),
            (
                [1.1, 1.6, 2.0, 2.5, 2.9],
                [0.38, 0.43, 0.47, 0.55, 0.61],
                "square",
                "Lab B",
            ),
        ],
        location="upper left",
        label=("Signal strength", "Response"),
        grid="major",
        fname=None,
    )
    save_example(fig, "scatter_plot")


def generate_errorbar_example() -> None:
    configure_plot_style(layout="paper-2col", theme="colorblind", latex=True)
    fig, _ = plot_errorbar(
        [
            (
                [1, 2, 3, 4],
                [82.1, 84.0, 85.2, 86.1],
                [0.7, 0.6, 0.5, 0.5],
                "circle",
                "Method A",
            ),
            (
                [1, 2, 3, 4],
                [80.4, 82.5, 83.4, 84.0],
                [0.8, 0.7, 0.6, 0.6],
                "square",
                "Method B",
            ),
        ],
        location="lower right",
        label=("Data fraction", r"Accuracy (\%)"),
        grid="major-y",
        fname=None,
    )
    save_example(fig, "errorbar_plot")


def generate_box_example() -> None:
    configure_plot_style(layout="paper-2col", theme="nature", latex=True)
    fig, _ = plot_box(
        [
            ([0.61, 0.65, 0.66, 0.67, 0.70, 0.72], "Baseline"),
            ([0.68, 0.70, 0.72, 0.73, 0.75, 0.77], "Model A"),
            ([0.71, 0.73, 0.74, 0.76, 0.78, 0.79], "Model B"),
        ],
        label=("Method", "F1 score"),
        fname=None,
    )
    save_example(fig, "box_plot")


def generate_heatmap_example() -> None:
    configure_plot_style(layout="paper-2col", theme="classic", latex=True)
    fig, _ = plot_heatmap(
        [
            [0.91, 0.06, 0.03],
            [0.08, 0.84, 0.08],
            [0.04, 0.10, 0.86],
        ],
        label=("Predicted", "True"),
        xticklabels=["A", "B", "C"],
        yticklabels=["A", "B", "C"],
        colorbar_label="Share",
        annotate=True,
        fname=None,
    )
    save_example(fig, "heatmap")


def generate_utility_example() -> None:
    configure_plot_style(layout="paper-2col-span", theme="classic", latex=True)
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.5))
    x = [1, 2, 3, 4]
    axes[0].plot(x, [0.52, 0.61, 0.68, 0.73], marker="o", label="Model")
    axes[0].plot(x, [0.49, 0.55, 0.60, 0.64], marker="s", label="Baseline")
    axes[1].scatter([0.12, 0.19, 0.27, 0.35], [0.44, 0.51, 0.59, 0.66], label="Lab A")
    axes[1].scatter([0.15, 0.23, 0.30, 0.38], [0.41, 0.48, 0.55, 0.62], label="Lab B")

    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Score")
    axes[1].set_xlabel("Signal")
    axes[1].set_ylabel("Response")
    for ax in axes:
        format_axes(ax, grid="major-y", despine=True)

    axes[0].legend(loc="lower right")
    axes[1].legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
    format_legend(axes[0].get_legend())
    format_legend(axes[1].get_legend())
    panel_labels(axes)
    annotate_points(axes[0], [(4, 0.73, "best")])
    save_example(fig, "utility_panel")


def generate_style_gallery() -> None:
    themes = ["classic", "nature", "colorblind", "mono", "warm"]
    fig, axes = plt.subplots(
        len(themes), 1, figsize=(6.8, 7.2), sharex=True, sharey=True
    )

    for ax, theme in zip(axes, themes):
        configure_plot_style(layout="paper-2col-span", theme=theme, latex=True)
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
    save_example(fig, "style_gallery")


def main() -> None:
    generate_line_example()
    generate_subplot_example()
    generate_bar_examples()
    generate_presentation_example()
    generate_monospace_example()
    generate_top_legend_example()
    generate_text_color_example()
    generate_scatter_example()
    generate_errorbar_example()
    generate_box_example()
    generate_heatmap_example()
    generate_utility_example()
    generate_style_gallery()


if __name__ == "__main__":
    main()
