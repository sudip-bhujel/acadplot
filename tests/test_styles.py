from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from acadplot import (
    available_layouts,
    available_themes,
    configure_plot_style,
    get_current_style,
    plot_bar,
    plot_grouped_bar,
    plot_line,
    plot_stacked_bar,
    use_style,
)


def test_configure_plot_style_updates_rcparams():
    style = configure_plot_style(layout="paper-1col", theme="classic", latex=False)

    assert style["layout"] == "paper-1col"
    assert style["theme"] == "classic"
    assert plt.rcParams["text.usetex"] is False
    assert plt.rcParams["axes.labelcolor"] == style["axis_label_color"]
    assert plt.rcParams["xtick.color"] == style["tick_color"]
    assert plt.rcParams["legend.labelcolor"] == style["legend_text_color"]
    assert style["axis_label_color"] == "#3F3F3F"
    assert style["tick_color"] == "#3F3F3F"
    assert "paper-1col" in available_layouts()
    assert "classic" in available_themes()


def test_layout_profiles_have_different_defaults():
    one_col = configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    two_col = configure_plot_style(layout="paper-2col", theme="classic", latex=False)

    assert one_col["fig_size"] != two_col["fig_size"]
    assert one_col["font_size"] < two_col["font_size"]


def test_inconsolata_font_preset_updates_rcparams():
    style = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        font="inconsolata",
        latex=False,
    )

    assert style["font"] == "inconsolata"
    assert style["font_family"] == "monospace"
    assert plt.rcParams["font.family"][0] == "monospace"
    assert plt.rcParams["font.monospace"][0] == "Inconsolata"


def test_all_themes_expose_valid_color_palettes():
    for theme in available_themes():
        style = configure_plot_style(layout="paper-1col", theme=theme, latex=False)
        colors = style["colors"]
        palette = style["palette"]

        assert len(colors) >= 5
        assert len(palette) >= 5
        assert all(str(color).startswith("#") for color in colors.values())
        assert str(style["axis_color"]).startswith("#")
        assert str(style["legend_text_color"]).startswith("#")


def test_use_style_restores_previous_style():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)

    with use_style(layout="paper-2col", theme="colorblind", latex=False):
        assert get_current_style()["layout"] == "paper-2col"
        assert get_current_style()["theme"] == "colorblind"

    assert get_current_style()["layout"] == "paper-1col"
    assert get_current_style()["theme"] == "classic"


def test_explicit_bar_overrides_and_default_grid():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    fig, ax = plot_bar(
        [([0, 1], [2, 3], "blue", "A")],
        "upper left",
        fig_size=(4.0, 3.0),
        font_size=9.0,
        fname=None,
    )

    width, height = fig.get_size_inches()
    assert abs(width - 4.0) < 0.01
    assert abs(height - 3.0) < 0.01
    assert ax.xaxis.label.get_size() == 9.0
    assert ax.xaxis.label.get_color() == get_current_style()["axis_label_color"]
    assert ax.spines["bottom"].get_edgecolor()
    legend = ax.get_legend()
    assert legend is not None
    assert legend.get_frame_on()
    assert (
        legend.get_frame().get_linewidth()
        == get_current_style()["legend_frame_linewidth"]
    )
    assert all(
        text.get_color() == get_current_style()["legend_text_color"]
        for text in legend.get_texts()
    )
    assert ax.get_axisbelow()
    assert any(line.get_visible() for line in ax.get_ygridlines())
    assert not any(line.get_visible() for line in ax.get_xgridlines())
    plt.close(fig)


def test_default_save_uses_tight_bbox_without_padding():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    captured = {}
    fig, ax = plt.subplots()
    original_savefig = fig.savefig

    def capture_savefig(*args, **kwargs):
        captured.update(kwargs)

    fig.savefig = capture_savefig
    try:
        plot_bar(
            [([0, 1], [2, 3], "blue", "A")],
            "upper left",
            ax=ax,
            fname="example.pdf",
        )
    finally:
        fig.savefig = original_savefig
        plt.close(fig)

    assert captured["bbox_inches"] == "tight"
    assert captured["pad_inches"] == 0


def test_omitted_line_colors_use_active_theme_palette():
    style = configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    fig, ax = plot_line(
        [
            ([0, 1], [1, 2], "circle", "A"),
            ([0, 1], [2, 3], "square", "B"),
        ],
        "upper left",
        fname=None,
    )

    assert [line.get_color() for line in ax.get_lines()] == list(style["palette"][:2])
    assert style["palette"][:3] == ("#332288", "#DDCC77", "#117733")
    plt.close(fig)


def test_existing_axes_use_active_theme_palette():
    fig, ax = plt.subplots()
    style = configure_plot_style(layout="paper-1col", theme="nature", latex=False)
    plot_line(
        [([0, 1], [1, 2], "circle", "A")],
        "upper left",
        ax=ax,
        fname=None,
    )

    assert ax.get_lines()[0].get_color() == style["palette"][0]
    plt.close(fig)


def test_explicit_line_color_still_overrides_palette():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    fig, ax = plot_line(
        [([0, 1], [1, 2], "#123456", "circle", "Explicit")],
        "upper left",
        fname=None,
    )

    assert ax.get_lines()[0].get_color() == "#123456"
    plt.close(fig)


def test_plot_smoke_and_vector_exports():
    configure_plot_style(layout="paper-1col", theme="nature", latex=False)

    line_data = [
        ([0, 1, 2], [1, 2, 3], "circle", "A"),
        ([0, 1, 2], [1.5, 2.5, 2.75], "square", "B"),
    ]
    bar_data = [([0, 1, 2], [1, 2, 3], "A")]
    grouped_data = [
        ("G1", [(1.0, "A"), (2.0, "B")]),
        ("G2", [(1.5, "A"), (2.5, "B")]),
    ]
    stacked_categories = ["G1", "G2"]
    stacked_data = [([1, 2], "A"), ([2, 1], "B")]

    with TemporaryDirectory() as tmp:
        pdf_path = Path(tmp) / "line.pdf"
        svg_path = Path(tmp) / "bar.svg"

        fig, _ = plot_line(line_data, "upper left", fname=str(pdf_path))
        plt.close(fig)
        fig, _ = plot_bar(bar_data, "upper left", fname=str(svg_path))
        plt.close(fig)
        fig, _ = plot_grouped_bar(grouped_data, "upper left", fname=None)
        plt.close(fig)
        fig, _ = plot_stacked_bar(
            stacked_categories,
            stacked_data,
            "upper left",
            fname=None,
        )
        plt.close(fig)

        assert pdf_path.exists()
        assert svg_path.exists()


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_"):
            test()
