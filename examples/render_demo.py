"""Render the openlab-style hero demo image.

Produces examples/demo.png — a single 2x2 grid showcasing openlab-style's
MATLAB-styled output across the four most common plot types (multi-line,
histogram, heatmap, log-scale frequency response).

This is what the README and social posts use as the single "this is what
openlab-style produces" image. We do NOT ship a side-by-side comparison
against matplotlib defaults — the pitch is "your AI's plots now look like
MATLAB," and the image speaks to viewers who already know what MATLAB
plots look like.

Usage:
    python examples/render_demo.py
"""

from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import openlab_style

openlab_style.apply(grid=True)


def _polish(ax) -> None:
    """Apply per-axes MATLAB polish (tick density, integer formatter)."""
    openlab_style.apply_to_axes(ax)


def main() -> int:
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))

    # ─── (0,0) Multi-line trig plot ──────────────────────────────────────
    t = np.linspace(0, 2 * np.pi, 200)
    ax = axes[0, 0]
    ax.plot(t, np.sin(t), label="sin(t)")
    ax.plot(t, np.cos(t), label="cos(t)")
    ax.plot(t, np.sin(2 * t), label="sin(2t)")
    ax.set_xlabel("t")
    ax.set_ylabel("amplitude")
    ax.set_title("Trig functions")
    ax.legend()

    # ─── (0,1) Histogram (use openlab_style.hist for MATLAB-style alpha) ─
    np.random.seed(42)
    ax = axes[0, 1]
    # Switch to this axes so openlab_style.hist's underlying plt.hist targets it
    plt.sca(ax)
    openlab_style.hist(np.random.randn(2000), bins=30)
    ax.set_xlabel("value")
    ax.set_ylabel("count")
    ax.set_title("Histogram of 2000 N(0,1) samples")

    # ─── (1,0) Peaks heatmap (parula colormap) ───────────────────────────
    x = np.linspace(-3, 3, 200)
    y = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x, y)
    Z = (
        3 * (1 - X) ** 2 * np.exp(-(X**2) - (Y + 1) ** 2)
        - 10 * (X / 5 - X**3 - Y**5) * np.exp(-(X**2) - Y**2)
        - np.exp(-((X + 1) ** 2) - Y**2) / 3
    )
    ax = axes[1, 0]
    im = ax.imshow(Z, extent=(-3, 3, -3, 3), origin="lower", aspect="auto")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("peaks() — surface")
    plt.colorbar(im, ax=ax)

    # ─── (1,1) Loglog frequency response ─────────────────────────────────
    f = np.logspace(0, 4, 200)
    ax = axes[1, 1]
    ax.loglog(f, np.abs(1 / (1 + 1j * f / 100)), label="cutoff 100 Hz")
    ax.loglog(f, np.abs(1 / (1 + 1j * f / 1000)), label="cutoff 1 kHz")
    ax.set_xlabel("frequency (Hz)")
    ax.set_ylabel("|H(f)|")
    ax.set_title("Two low-pass filters")
    ax.legend()

    # Apply per-axes MATLAB tick label formatter (drops trailing zeros).
    # No tick-density override — matplotlib auto density matches MATLAB
    # (verified against MathWorks doc plot screenshots: MATLAB shows ~6-11
    # ticks per axis depending on range, same as matplotlib auto).
    _polish(axes[0, 0])  # trig
    _polish(axes[0, 1])  # histogram
    _polish(axes[1, 0])  # peaks heatmap (linear axes)
    # loglog: log axes manage their own formatter (e.g. 10^1, 10^2). Leave alone.

    fig.tight_layout()

    out_path = os.path.join(os.path.dirname(__file__), "demo.png")
    fig.savefig(out_path, dpi=110, facecolor="white")
    print(f"wrote {out_path}")
    plt.close(fig)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
