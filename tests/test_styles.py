from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from acadplot import (
    available_fonts,
    available_layouts,
    available_text_colors,
    available_themes,
    annotate_points,
    configure_plot_style,
    despine,
    figure_size,
    format_axes,
    format_legend,
    get_output_dir,
    get_current_style,
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
    save_all,
    set_output_dir,
    theme_preview,
    use_style,
)


def test_configure_plot_style_updates_rcparams():
    style = configure_plot_style(layout="paper-1col", theme="classic", latex=False)

    assert style["layout"] == "paper-1col"
    assert style["theme"] == "classic"
    assert style["font"] == "inconsolata"
    assert style["font_family"] == "monospace"
    assert plt.rcParams["text.usetex"] is False
    assert plt.rcParams["font.monospace"][0] == "Inconsolata"
    assert plt.rcParams["axes.labelcolor"] == style["axis_label_color"]
    assert plt.rcParams["xtick.color"] == style["tick_color"]
    assert plt.rcParams["legend.labelcolor"] == style["legend_text_color"]
    assert style["axis_label_color"] == "#3F3F3F"
    assert style["tick_color"] == "#3F3F3F"
    assert "paper-1col" in available_layouts()
    assert "classic" in available_themes()
    assert "inconsolata" in available_fonts()
    assert "dark" in available_text_colors()
    assert "gray" in available_text_colors()


def test_layout_profiles_have_different_defaults():
    one_col = configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    two_col = configure_plot_style(layout="paper-2col", theme="classic", latex=False)
    two_col_subplot = configure_plot_style(
        layout="paper-2col-subplot", theme="classic", latex=False
    )
    span = configure_plot_style(layout="paper-2col-span", theme="classic", latex=False)

    assert two_col["fig_size"][0] < one_col["fig_size"][0]
    assert two_col_subplot["fig_size"][0] == two_col["fig_size"][0]
    assert two_col_subplot["fig_size"][1] < two_col["fig_size"][1]
    assert span["fig_size"][0] > one_col["fig_size"][0]
    assert one_col["font_size"] < two_col["font_size"]
    assert two_col_subplot["font_size"] < one_col["font_size"]
    assert two_col_subplot["tick_size"] < two_col_subplot["label_size"]
    assert two_col_subplot["legend_size"] < two_col_subplot["label_size"]
    assert two_col_subplot["line_width"] < two_col["line_width"]
    assert span["font_size"] < two_col["font_size"]
    assert one_col["line_width"] < two_col["line_width"]
    assert figure_size("paper-2col-subplot") == two_col_subplot["fig_size"]
    assert figure_size("paper-2col") == two_col["fig_size"]


def test_inconsolata_default_font_preset_updates_rcparams():
    style = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        latex=False,
    )

    assert style["font"] == "inconsolata"
    assert style["font_family"] == "monospace"
    assert plt.rcParams["font.family"][0] == "monospace"
    assert plt.rcParams["font.monospace"][0] == "Inconsolata"


def test_configure_plot_style_accepts_font_size_override():
    style = configure_plot_style(
        layout="paper-2col",
        theme="classic",
        latex=False,
        font_size=10.5,
    )

    assert style["font_size"] == 10.5
    assert plt.rcParams["font.size"] == 10.5
    assert plt.rcParams["axes.labelsize"] == 10.5
    assert plt.rcParams["legend.fontsize"] == 10.5

    fig, ax = plot_line(
        [([0, 1], [1, 2], "circle", "A")],
        "upper left",
        fname=None,
    )
    assert ax.xaxis.label.get_size() == 10.5
    plt.close(fig)


def test_configure_plot_style_accepts_separate_size_overrides():
    style = configure_plot_style(
        layout="paper-2col",
        theme="classic",
        latex=False,
        font_size=9.5,
        label_size=11.0,
        tick_size=8.0,
        legend_size=7.5,
        title_size=12.0,
    )

    assert style["font_size"] == 9.5
    assert style["label_size"] == 11.0
    assert style["tick_size"] == 8.0
    assert style["legend_size"] == 7.5
    assert style["title_size"] == 12.0
    assert plt.rcParams["axes.labelsize"] == 11.0
    assert plt.rcParams["xtick.labelsize"] == 8.0
    assert plt.rcParams["legend.fontsize"] == 7.5
    assert plt.rcParams["axes.titlesize"] == 12.0

    fig, ax = plot_line(
        [([0, 1], [1, 2], "circle", "A")],
        "upper left",
        fname=None,
    )
    assert ax.xaxis.label.get_size() == 11.0
    assert ax.xaxis.get_ticklabels()[0].get_size() == 8.0
    assert ax.get_legend().get_texts()[0].get_size() == 7.5
    plt.close(fig)


def test_configure_plot_style_accepts_text_color_override():
    style = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        latex=False,
        text_color="#202020",
    )

    assert style["text_color"] == "#202020"
    assert style["axis_label_color"] == "#202020"
    assert style["tick_color"] == "#202020"
    assert style["legend_text_color"] == "#202020"
    assert style["title_color"] == "#202020"
    assert plt.rcParams["text.color"] == "#202020"
    assert plt.rcParams["axes.labelcolor"] == "#202020"
    assert plt.rcParams["axes.titlecolor"] == "#202020"
    assert plt.rcParams["xtick.color"] == "#202020"
    assert plt.rcParams["legend.labelcolor"] == "#202020"

    fig, ax = plot_line(
        [([0, 1], [1, 2], "circle", "A")],
        "upper left",
        fname=None,
    )
    ax.set_title("Readable title")
    format_axes(ax)

    assert ax.xaxis.label.get_color() == "#202020"
    assert ax.xaxis.get_ticklabels()[0].get_color() == "#202020"
    assert ax.get_title() == "Readable title"
    assert ax.title.get_color() == "#202020"
    assert ax.get_legend().get_texts()[0].get_color() == "#202020"
    plt.close(fig)


def test_configure_plot_style_accepts_text_color_presets_and_raw_colors():
    preset = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        latex=False,
        text_color="dark",
    )
    assert preset["text_color"] == "#202020"
    assert preset["tick_color"] == "#202020"

    gray = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        latex=False,
        text_color="gray",
    )
    assert gray["text_color"] == "#555555"

    raw = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        latex=False,
        text_color="tab:blue",
    )
    assert raw["text_color"] == "#1f77b4"

    rgb = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        latex=False,
        text_color=(0.1, 0.2, 0.3),
    )
    assert rgb["text_color"] == "#1a334c"


def test_scale_increases_font_and_line_defaults():
    base = configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    scaled = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        latex=False,
        scale=1.2,
    )

    assert scaled["font_size"] > base["font_size"]
    assert scaled["line_width"] > base["line_width"]
    assert scaled["marker_scale"] > base["marker_scale"]


def test_latex_auto_resolves_to_boolean():
    style = configure_plot_style(
        layout="paper-1col",
        theme="classic",
        latex="auto",
    )

    assert style["latex_requested"] == "auto"
    assert isinstance(style["latex"], bool)
    assert plt.rcParams["text.usetex"] == style["latex"]


def test_use_style_accepts_temporary_font_size_override():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)

    with use_style(theme="colorblind", font_size=11.0):
        assert get_current_style()["font_size"] == 11.0
        assert plt.rcParams["font.size"] == 11.0

    assert get_current_style()["font_size"] == 7.5


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


def test_save_utility_writes_multiple_formats_and_closes():
    fig, _ = plt.subplots()

    with TemporaryDirectory() as tmp:
        saved = save(fig, "figure", directory=tmp, pdf=True, svg=True)

        assert saved == (
            Path(tmp) / "figure.png",
            Path(tmp) / "figure.pdf",
            Path(tmp) / "figure.svg",
        )
        assert all(path.exists() for path in saved)
        assert not plt.fignum_exists(fig.number)


def test_save_utility_respects_explicit_suffix():
    fig, _ = plt.subplots()

    with TemporaryDirectory() as tmp:
        target = Path(tmp) / "exact.pdf"
        saved = save(fig, target, png=False)

        assert saved == (target,)
        assert target.exists()


def test_save_utility_formats_are_explicit():
    fig, _ = plt.subplots()

    with TemporaryDirectory() as tmp:
        saved = save(fig, "figure", directory=tmp, formats=("pdf", "svg"))

        assert saved == (
            Path(tmp) / "figure.pdf",
            Path(tmp) / "figure.svg",
        )
        assert not (Path(tmp) / "figure.png").exists()


def test_output_dir_and_save_all():
    previous = get_output_dir()
    fig, _ = plt.subplots()

    with TemporaryDirectory() as tmp:
        try:
            set_output_dir(tmp)
            saved = save_all(fig, "figure")

            assert get_output_dir() == Path(tmp)
            assert saved == (
                Path(tmp) / "figure.png",
                Path(tmp) / "figure.pdf",
                Path(tmp) / "figure.svg",
            )
            assert all(path.exists() for path in saved)
        finally:
            set_output_dir(previous)


def test_save_metadata_sidecar():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    fig, _ = plt.subplots()

    with TemporaryDirectory() as tmp:
        saved = save(fig, Path(tmp) / "figure.pdf", metadata=True)
        metadata_path = saved[0].with_suffix(".acadplot.json")

        assert metadata_path.exists()
        assert '"outputs"' in metadata_path.read_text(encoding="utf-8")


def test_format_axes_despine_panel_labels_and_annotations():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    fig, axes = plt.subplots(1, 2)
    axes[0].plot([0, 1], [1, 2])

    format_axes(axes[0], grid="major-y", despine=True)
    despine(axes[1])
    legend = axes[0].legend(["line"])
    format_legend(legend)
    labels = panel_labels(axes)
    annotations = annotate_points(axes[0], [(1, 2, "peak")])

    assert not axes[0].spines["top"].get_visible()
    assert not axes[0].spines["right"].get_visible()
    assert not axes[1].spines["top"].get_visible()
    assert [text.get_text() for text in labels] == ["(a)", "(b)"]
    assert annotations[0].get_text() == "peak"
    assert legend.get_texts()[0].get_color() == get_current_style()["legend_text_color"]
    plt.close(fig)


def test_theme_preview_smoke():
    fig, ax = theme_preview(themes=("classic", "nature"))

    assert len(ax.patches) > 0
    plt.close(fig)


def test_legend_outside_for_line_plot():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    fig, ax = plot_line(
        [([0, 1], [1, 2], "circle", "A")],
        "upper left",
        legend_outside="right",
        fname=None,
    )

    assert ax.get_legend() is not None
    assert ax.get_legend()._loc == 6
    plt.close(fig)


def test_top_legend_multiple_columns_for_line_plot():
    configure_plot_style(layout="paper-1col", theme="classic", latex=False)
    fig, ax = plot_line(
        [
            ([0, 1], [1, 2], "circle", "A"),
            ([0, 1], [2, 3], "square", "B"),
            ([0, 1], [3, 4], "triangle_up", "C"),
        ],
        "lower center",
        ncols=3,
        legend_outside="top",
        fname=None,
    )

    legend = ax.get_legend()
    assert legend is not None
    assert legend._loc == 8
    assert legend._ncols == 3
    plt.close(fig)


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
    assert style["palette"][:3] == ("#2F3A8F", "#28745A", "#B04A5A")
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
        fig, _ = plot_scatter(
            [([0, 1, 2], [1, 2, 3], "circle", "A")],
            "upper left",
            fname=None,
        )
        plt.close(fig)
        fig, _ = plot_errorbar(
            [([0, 1, 2], [1, 2, 3], [0.1, 0.2, 0.1], "circle", "A")],
            "upper left",
            fname=None,
        )
        plt.close(fig)
        fig, _ = plot_box(
            [([1, 2, 3], "A"), ([2, 3, 4], "B")],
            fname=None,
        )
        plt.close(fig)
        fig, _ = plot_heatmap(
            [[1, 0], [0, 1]],
            xticklabels=["A", "B"],
            yticklabels=["A", "B"],
            annotate=True,
            fname=None,
        )
        plt.close(fig)

        assert pdf_path.exists()
        assert svg_path.exists()


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_"):
            test()
