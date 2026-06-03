"""Smoke tests for openlab_style.apply() and reset()."""

from __future__ import annotations

import matplotlib as mpl
import pytest

import openlab_style


def test_version_present() -> None:
    assert isinstance(openlab_style.__version__, str)
    assert openlab_style.__version__.count(".") >= 1


def test_apply_changes_rcparams() -> None:
    mpl.rcdefaults()
    default_facecolor = mpl.rcParams["axes.facecolor"]
    default_tickdir = mpl.rcParams["xtick.direction"]

    openlab_style.apply()

    assert mpl.rcParams["axes.facecolor"] == "white"
    assert mpl.rcParams["xtick.direction"] == "in"
    assert mpl.rcParams["ytick.direction"] == "in"
    assert mpl.rcParams["image.cmap"] == "parula"

    openlab_style.reset()
    # After reset, params return to defaults (or at least no longer match
    # the openlab-style override for tickdir, which matplotlib's default is "out")
    assert mpl.rcParams["xtick.direction"] != "in" or default_tickdir == "in"


def test_parula_registered() -> None:
    openlab_style.apply()
    cmap = mpl.colormaps["parula"]
    assert cmap.name == "parula"
    # Post-R2017a parula extraction has ~78 entries. Whatever the published
    # data file says — pin the test to that length rather than a magic number.
    from openlab_style._parula import PARULA_DATA
    assert cmap.N == len(PARULA_DATA)
    assert cmap.N >= 64  # at least the pre-R2019b default


def test_color_cycle_is_matlab_lines() -> None:
    openlab_style.apply()
    cycle = mpl.rcParams["axes.prop_cycle"].by_key()["color"]
    # First color should be MATLAB blue
    assert cycle[0].lower() == "#0072bd"
    # Should have 7 colors (MATLAB's lines palette)
    assert len(cycle) == 7


def test_apply_idempotent() -> None:
    openlab_style.apply()
    openlab_style.apply()
    # Should not raise, and parula should still be registered exactly once
    from openlab_style._parula import PARULA_DATA
    cmap = mpl.colormaps["parula"]
    assert cmap.N == len(PARULA_DATA)


def test_fontsize_arg() -> None:
    openlab_style.apply(fontsize=12)
    assert mpl.rcParams["font.size"] == 12
    # MATLAB R2014b+ defaults: LabelFontSizeMultiplier = 1.1, so labels render
    # at 1.1× the base font size (audit row 19). For base=12: 12*1.1 = 13.2.
    assert mpl.rcParams["axes.labelsize"] == pytest.approx(13.2)
    # Same: TitleFontSizeMultiplier = 1.1 (audit row 17).
    assert mpl.rcParams["axes.titlesize"] == pytest.approx(13.2)


def test_grid_default_off() -> None:
    openlab_style.apply()
    assert mpl.rcParams["axes.grid"] is False


def test_grid_opt_in() -> None:
    openlab_style.apply(grid=True)
    assert mpl.rcParams["axes.grid"] is True
