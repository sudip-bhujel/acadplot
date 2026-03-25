import matplotlib.pyplot as plt


def configure_plot_style():
    """
    Configure global plot style settings.

    Uses LaTeX for text rendering and sets line widths for axes and ticks.
    """
    plt.rc("text", usetex=True)
    plt.rc("axes", linewidth=0.5)
    plt.rc("xtick.major", width=0.5)
    plt.rc("xtick.minor", width=0.3)
    plt.rc("ytick.major", width=0.5)
    plt.rc("ytick.minor", width=0.3)
    plt.rc("font", family="serif")
