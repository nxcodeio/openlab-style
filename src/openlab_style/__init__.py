"""openlab-style: matplotlib styling that mimics MATLAB R2014b+ defaults.

The pain: AI assistants (ChatGPT, Claude) generate Python + matplotlib for
technical computing. But for MATLAB users (students with assignments,
researchers collaborating with MATLAB users), matplotlib output visually
screams "not MATLAB" — different colormap, fonts, axes style, line colors.

The fix: a one-liner that aligns matplotlib's defaults to MATLAB's. Output
looks like it came out of MATLAB R2014b+ (parula colormap, lines palette,
inward ticks, white background, full axes box).

Usage:
    import openlab_style
    openlab_style.apply()

    import matplotlib.pyplot as plt
    import numpy as np
    t = np.linspace(0, 2*np.pi, 100)
    plt.plot(t, np.sin(t), t, np.cos(t))
    plt.legend(['sin(t)', 'cos(t)'])
    plt.title('Trig functions')
    plt.show()

    # ↑ output now looks like MATLAB

To reset:
    openlab_style.reset()
"""

from __future__ import annotations

import matplotlib as mpl
from matplotlib import cycler
from matplotlib.colors import ListedColormap

from ._parula import PARULA_DATA

__version__ = "0.1.0"
__all__ = [
    "apply",
    "reset",
    "MATLAB_LINES",
    "MATLAB_LINES_HEX",
    "parula_cmap",
    "hist",
    "matlab_formatter",
    "apply_to_axes",
]

# MATLAB R2014b+ default ColorOrder ("lines" palette).
# Values from MATLAB's `get(groot, 'DefaultAxesColorOrder')`.
MATLAB_LINES = [
    (0.0000, 0.4470, 0.7410),  # blue
    (0.8500, 0.3250, 0.0980),  # orange
    (0.9290, 0.6940, 0.1250),  # yellow
    (0.4940, 0.1840, 0.5560),  # purple
    (0.4660, 0.6740, 0.1880),  # green
    (0.3010, 0.7450, 0.9330),  # light blue
    (0.6350, 0.0780, 0.1840),  # dark red
]

MATLAB_LINES_HEX = [
    "#0072BD",
    "#D95319",
    "#EDB120",
    "#7E2F8E",
    "#77AC30",
    "#4DBEEE",
    "#A2142F",
]


def parula_cmap() -> ListedColormap:
    """Return MATLAB's parula colormap as a matplotlib ListedColormap.

    Parula was introduced as the MATLAB default in R2014b. It is not
    distributed with matplotlib (closest built-in is viridis).
    """
    return ListedColormap(PARULA_DATA, name="parula")


def _register_parula() -> None:
    """Register the parula colormap with matplotlib (idempotent)."""
    try:
        mpl.colormaps["parula"]
    except (KeyError, ValueError):
        mpl.colormaps.register(parula_cmap())


def apply(*, grid: bool = False, fontsize: int = 10) -> None:
    """Apply MATLAB-style defaults to matplotlib.

    Mutates global matplotlib rcParams. Idempotent. Call `reset()` to undo.

    Args:
        grid: If True, turn the grid on by default (MATLAB's grid is
            light gray, behind data). Default False matches MATLAB's
            "grid off" default; many users still want it on.
        fontsize: Base font size. MATLAB's default is 10pt.
    """
    _register_parula()

    mpl.rcParams.update(
        {
            # ─── Figure ──────────────────────────────────────────────
            "figure.facecolor": "white",
            "figure.edgecolor": "white",
            # ─── Axes ────────────────────────────────────────────────
            "axes.facecolor": "white",
            "axes.edgecolor": "black",
            "axes.linewidth": 0.5,
            "axes.spines.top": True,
            "axes.spines.right": True,
            "axes.spines.left": True,
            "axes.spines.bottom": True,
            # MATLAB R2014b+ default TitleFontWeight is 'bold' (per Axes Properties
            # documentation). Title size = base * TitleFontSizeMultiplier (1.1).
            # Label size = base * LabelFontSizeMultiplier (1.1).
            # See docs/matlab-fidelity-audit.md rows 17-19.
            "axes.titleweight": "bold",
            "axes.titlesize": round(fontsize * 1.1, 1),
            "axes.labelsize": round(fontsize * 1.1, 1),
            "axes.prop_cycle": cycler(color=MATLAB_LINES_HEX),
            "axes.grid": grid,
            "axes.axisbelow": True,
            "axes.labelcolor": "black",
            # ─── Lines ────────────────────────────────────────────────
            # MATLAB R2014b+ Line property defaults (audit row 8):
            # - LineWidth = 0.5 pt
            # - MarkerSize = 6 pt
            # Note: 0.5pt is the technical default but renders thin on Hi-DPI
            # displays. Users who want thicker lines call plt.plot(..., lw=1.5).
            "lines.linewidth": 0.5,
            "lines.markersize": 6,
            "lines.markeredgewidth": 0.5,
            # ─── Ticks ───────────────────────────────────────────────
            # MATLAB defaults (per Axes Properties docs, audit rows 33-40):
            # - TickDir = 'in'
            # - TickLength = [0.01 0.025] normalized; ≈ 5pt at typical figure sizes
            # - XMinorTick / YMinorTick = 'off' for linear, 'on' for log
            # matplotlib has no per-axis-type default for minor ticks. We choose
            # OFF globally to match MATLAB linear plots (the common case). For
            # log plots, matplotlib auto-shows minor ticks anyway when the scale
            # is set to log via plt.xscale('log'). Result matches MATLAB.
            "xtick.direction": "in",
            "ytick.direction": "in",
            "xtick.major.size": 5,
            "ytick.major.size": 5,
            "xtick.minor.size": 3,
            "ytick.minor.size": 3,
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "xtick.minor.width": 0.5,
            "ytick.minor.width": 0.5,
            "xtick.color": "black",
            "ytick.color": "black",
            "xtick.labelsize": fontsize,
            "ytick.labelsize": fontsize,
            # MATLAB-correct: minor ticks OFF for linear axes. matplotlib still
            # auto-shows them on log axes (semilogx/y/loglog). See audit row 39.
            "xtick.minor.visible": False,
            "ytick.minor.visible": False,
            # ─── Grid (used only if axes.grid is True) ───────────────
            # MATLAB R2014b+ defaults (Axes Properties docs, audit rows 41-47):
            # - GridLineStyle = '-' (SOLID)         ← we previously had ':' WRONG
            # - GridLineWidth = 0.5
            # - GridAlpha = 0.15                    ← we previously had 1.0 WRONG (6.7x too opaque)
            # - GridColor = inherits axis color (black for light theme)
            # - MinorGridLineStyle = ':' (dotted)
            # - MinorGridAlpha = 0.25
            "grid.color": "black",
            "grid.linestyle": "-",
            "grid.linewidth": 0.5,
            "grid.alpha": 0.15,
            # ─── Fonts ───────────────────────────────────────────────
            # MATLAB uses Helvetica on macOS, Helvetica on Linux (or
            # closest), and Arial-equivalent on Windows. Matplotlib
            # picks the first available from the list.
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Helvetica",
                "Arial",
                "Liberation Sans",
                "DejaVu Sans",
            ],
            "font.size": fontsize,
            # ─── Legend ──────────────────────────────────────────────
            # MATLAB R2014b+ Legend property defaults (audit rows 48-54):
            # - Box = 'on' (frame visible)
            # - Color (bg) = [1 1 1] (white)
            # - EdgeColor = [0.15 0.15 0.15] (dark gray, NOT pure black)
            # - LineWidth = 0.5 pt
            # - FontSize auto-scaled to 90% of axes FontSize (no equivalent
            #   rcParam; we approximate as base * 0.9)
            # - BackgroundAlpha = 1.0
            "legend.frameon": True,
            "legend.framealpha": 1.0,
            "legend.edgecolor": (0.15, 0.15, 0.15),
            "legend.facecolor": "white",
            "legend.fancybox": False,
            "legend.fontsize": round(fontsize * 0.9, 1),
            # MATLAB legend line samples are shorter than matplotlib's default.
            # matplotlib default = 2.0 (font-size units). MATLAB feels closer
            # to 1.0. Audit row note (Round 3).
            "legend.handlelength": 1.0,
            # ─── Patches (histograms, bar charts) ────────────────────
            # MATLAB R2014b+ histogram() defaults (audit rows 55-58):
            # - EdgeColor = 'none' (no edges by default — this surprised us;
            #   we had edges ON in earlier versions thinking that matched
            #   MATLAB. The MODERN histogram() function is edgeless.)
            # - FaceAlpha = 0.6 (semi-transparent — no matplotlib rcParam
            #   for this; users must pass alpha=0.6 explicitly per-call)
            # - LineWidth = 0.5 pt (only matters if user adds edges via call)
            # The older hist() function (deprecated) does have edges by
            # default. We optimize for the modern histogram() use case.
            "patch.edgecolor": "none",
            "patch.linewidth": 0.5,
            "patch.force_edgecolor": False,
            # ─── Default colormap (parula since R2014b) ──────────────
            "image.cmap": "parula",
        }
    )


def reset() -> None:
    """Reset matplotlib to its factory defaults (undo apply())."""
    mpl.rcdefaults()


def hist(*args, **kwargs):
    """MATLAB-style histogram. Drop-in for `matplotlib.pyplot.hist`.

    Matches MATLAB R2014b+ `histogram()` defaults that matplotlib rcParams
    can't capture:
      - alpha = 0.6 (FaceAlpha = 0.6 in MATLAB)
      - edgecolor = 'none' (matches our apply() patch settings)
      - color inherits from current axes color cycle (= MATLAB blue)

    Returns whatever `plt.hist` returns.

    Usage:
        import openlab_style
        openlab_style.apply()
        openlab_style.hist(data, bins=30)

    User-supplied kwargs win — pass `alpha=1.0` to override.
    """
    import matplotlib.pyplot as plt
    kwargs.setdefault("alpha", 0.6)
    kwargs.setdefault("edgecolor", "none")
    return plt.hist(*args, **kwargs)


def matlab_formatter():
    """Return a matplotlib FuncFormatter that mimics MATLAB tick label format.

    MATLAB shows tick labels without trailing zeros: `-1`, `-0.75`, `0`, `0.5`,
    `1` (not `-1.00`, `-0.75`, `0.00`, etc). matplotlib's default
    ScalarFormatter pads all labels to the same precision, which looks wrong
    when integer ticks are mixed with decimal ticks.

    Usage:
        import openlab_style
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(...)
        ax.yaxis.set_major_formatter(openlab_style.matlab_formatter())
        ax.xaxis.set_major_formatter(openlab_style.matlab_formatter())

    Or use `openlab_style.apply_to_axes(ax)` to set this on both axes plus
    other per-axes MATLAB-style polish.
    """
    from matplotlib.ticker import FuncFormatter

    def _fmt(value, _pos):
        # Treat tiny float drift as zero, render as "0" not "-0" / "0.00".
        if abs(value) < 1e-12:
            return "0"
        # Integer-valued ticks: no decimal point. e.g. -1.0 -> "-1".
        if value == int(value):
            return str(int(value))
        # Non-integer: %g drops trailing zeros. 0.500 -> "0.5"; 0.25 -> "0.25".
        return f"{value:g}"

    return FuncFormatter(_fmt)


def apply_to_axes(ax, *, nbins=None, formatter: bool = True) -> None:
    """Apply per-axes MATLAB-style polish that rcParams cannot capture.

    matplotlib's rcParams set global styling (colors, grid, fonts) but NOT
    per-axes details like custom formatters. Call this on each axes you want
    the trailing-zero stripped (e.g. "0" instead of "0.00") MATLAB-style
    tick labels.

    Args:
        ax: a matplotlib Axes object.
        nbins: target number of major ticks per axis. Default `None` lets
            matplotlib's auto picker choose (which produces similar density
            to MATLAB — verified against MathWorks doc plot screenshots).
            Set explicitly only if you want forced sparser/denser ticks.
        formatter: if True, attach `matlab_formatter()` to both x and y axes
            so integer ticks render without trailing zeros.

    Usage:
        fig, axes = plt.subplots(2, 2)
        for ax in axes.flat:
            openlab_style.apply_to_axes(ax)
    """
    if nbins is not None:
        from matplotlib.ticker import MaxNLocator
        ax.xaxis.set_major_locator(MaxNLocator(nbins=nbins))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=nbins))
    if formatter:
        fmt = matlab_formatter()
        ax.xaxis.set_major_formatter(fmt)
        ax.yaxis.set_major_formatter(fmt)
