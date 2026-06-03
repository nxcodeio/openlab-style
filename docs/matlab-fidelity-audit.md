# MATLAB Fidelity Audit

**Goal**: every visible aspect of openlab-style's output must match MATLAB R2014b+ defaults at pixel level. Where we differ from MATLAB documented defaults, either fix the rcParam or document why the difference is intentional/unavoidable.

**Target version**: MATLAB R2014b+ (the "modern MATLAB" baseline — covers R2014b through R2025+; all use parula colormap, lines palette, modern axes).

**Method**:
1. Each row sources MATLAB's documented default from MathWorks docs, MathWorks blog posts, or third-party MATLAB-extraction projects.
2. Compare to current openlab-style value (in `src/openlab_style/__init__.py`).
3. Classify: ✅ MATCH / ⚠️ ADJUST (close but off) / ❌ WRONG (needs fix) / 📝 NOTE (intentional or unavoidable difference).
4. ADJUST and WRONG rows generate code patches in subsequent commits.

**Status**: 🟡 IN PROGRESS — audit started 2026-06-03. Tracking shows when each section is complete.

---

## Section 1: Colors (line ColorOrder)

> MATLAB's default `lines` palette has 7 colors, used in cycling order for plot() calls. Documented in `colororder` function reference (R2019b+).

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 1 | Line 1 RGB | `#0072BD` (0.0000, 0.4470, 0.7410) | TBD | TBD | TBD | |
| 2 | Line 2 RGB | `#D95319` (0.8500, 0.3250, 0.0980) | TBD | TBD | TBD | |
| 3 | Line 3 RGB | `#EDB120` (0.9290, 0.6940, 0.1250) | TBD | TBD | TBD | |
| 4 | Line 4 RGB | `#7E2F8E` (0.4940, 0.1840, 0.5560) | TBD | TBD | TBD | |
| 5 | Line 5 RGB | `#77AC30` (0.4660, 0.6740, 0.1880) | TBD | TBD | TBD | |
| 6 | Line 6 RGB | `#4DBEEE` (0.3010, 0.7450, 0.9330) | TBD | TBD | TBD | |
| 7 | Line 7 RGB | `#A2142F` (0.6350, 0.0780, 0.1840) | TBD | TBD | TBD | |
| 8 | Default line linewidth | 1.5 pt | TBD | Plot Properties → LineWidth | TBD | |

---

## Section 2: Colormap (parula)

> Parula is MATLAB's default colormap since R2014b. Not in matplotlib; we ship a 64-entry approximation in `_parula.py`. Need authoritative RGB values.

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 9 | parula N entries | 64 | 64 (MATLAB default) | colormap docs | TBD | matplotlib uses 256 for built-ins; 64 matches MATLAB |
| 10 | parula entry 1 (deep blue) | (0.2422, 0.1504, 0.6603) | TBD | TBD | TBD | |
| 11 | parula entry 16 | (0.2206, 0.4603, 0.9973) | TBD | TBD | TBD | mid-blue band |
| 12 | parula entry 32 (mid) | (0.1408, 0.7670, 0.6554) | TBD | TBD | TBD | green-cyan transition |
| 13 | parula entry 48 | (0.8634, 0.7406, 0.1596) | TBD | TBD | TBD | yellow band |
| 14 | parula entry 64 (bright yellow) | (0.9769, 0.9839, 0.0805) | TBD | TBD | TBD | terminal yellow |
| 15 | image.cmap default | "parula" | "parula" (after register) | apply() registers | ✅ MATCH | |

---

## Section 3: Fonts

> MATLAB picks system Helvetica on macOS, Helvetica on Linux (with fallback), Helvetica Neue or Arial on Windows. Default font size varies by element.

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 16 | Font family (axes/text/title) | sans-serif → Helvetica, Arial, Liberation Sans, DejaVu Sans | Helvetica (macOS) | Text Properties → FontName | TBD | per-OS variation needs verification |
| 17 | Title font size | base+1 (default 11) | TBD | TBD | TBD | |
| 18 | Title font weight | normal | TBD (R2014b+ likely normal; appears heavy bc size) | TBD | TBD | |
| 19 | Axis label font size | base (default 10) | TBD | TBD | TBD | |
| 20 | Tick label font size | base (default 10) | TBD | TBD | TBD | |
| 21 | Legend font size | base (default 10) | TBD | TBD | TBD | |
| 22 | Default font size (base) | 10 | TBD | TBD | TBD | |
| 23 | Math text fontset | matplotlib default (DejaVu Sans) | MATLAB uses LaTeX-like for `$...$` | TBD | TBD | hard to match exactly w/o LaTeX |

---

## Section 4: Axes (box, spines, line widths)

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 24 | axes.spines.top | True | True (box on) | Axes Properties → Box | ✅ MATCH | |
| 25 | axes.spines.right | True | True | same | ✅ MATCH | |
| 26 | axes.spines.left | True | True | same | ✅ MATCH | |
| 27 | axes.spines.bottom | True | True | same | ✅ MATCH | |
| 28 | axes line width | 0.5 pt | TBD | Axes → LineWidth | TBD | matplotlib default is 0.8 |
| 29 | axes edge color | black | TBD | Axes → XColor/YColor | TBD | |
| 30 | axes face color | white | TBD | Axes → Color | TBD | |
| 31 | figure face color | white | TBD | Figure → Color | TBD | |
| 32 | axisbelow (grid behind data) | True | TBD (MATLAB grid is behind data by default) | TBD | TBD | |

---

## Section 5: Ticks

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 33 | tick direction | in | "in" (MATLAB default) | Axes Properties → TickDir | TBD | matplotlib default is "out" |
| 34 | major tick length | 5 pt | TBD (MATLAB TickLength is normalized 0.01 of axis length, ≈ 5-7px) | Axes → TickLength | TBD | unit mismatch — need calculation |
| 35 | minor tick length | 3 pt | TBD | TBD | TBD | |
| 36 | major tick width | 0.5 pt | TBD | TBD | TBD | |
| 37 | minor tick width | 0.5 pt | TBD | TBD | TBD | |
| 38 | tick color | black | TBD | Axes → XColor/YColor | TBD | inherits axes |
| 39 | minor tick visible (linear axes) | True (our setting) | False (MATLAB default for linear) | Axes → XMinorTick | ❌ WRONG | over-applied on linear axes |
| 40 | minor tick visible (log axes) | True | True | XMinorTick auto for log | ✅ MATCH | |

---

## Section 6: Grid

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 41 | grid default state | False (off) | False | Axes → XGrid/YGrid | ✅ MATCH | user opts in via apply(grid=True) |
| 42 | grid color | #cccccc | TBD | Axes → GridColor | TBD | |
| 43 | grid line style | : (dotted) | TBD (MATLAB GridLineStyle default is "-" solid R2014b; was ":" in older) | Axes → GridLineStyle | ⚠️ VERIFY | possible mistake |
| 44 | grid line width | 0.5 pt | TBD | Axes → GridLineWidth (R2014b+ exposes this) | TBD | |
| 45 | grid alpha | 1.0 | TBD (MATLAB GridAlpha default is 0.15 R2014b+) | Axes → GridAlpha | ⚠️ VERIFY | |
| 46 | minor grid line style | inherit | TBD | Axes → MinorGridLineStyle | TBD | |
| 47 | minor grid alpha | inherit | TBD | Axes → MinorGridAlpha | TBD | |

---

## Section 7: Legend

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 48 | legend frame on | True | True | Legend → Box | ✅ MATCH | |
| 49 | legend frame alpha | 1.0 | TBD | Legend → BoxOpacity | TBD | |
| 50 | legend edge color | black | TBD | Legend → EdgeColor | TBD | |
| 51 | legend face color | white | TBD | Legend → Color | TBD | |
| 52 | legend frame fancy box | False (square corners) | TBD (MATLAB default is square) | TBD | TBD | |
| 53 | legend font size | base (10) | TBD | TBD | TBD | |
| 54 | legend edge linewidth | matplotlib default (0.8) | TBD | Legend → LineWidth | TBD | |

---

## Section 8: Patches (histograms, bars)

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 55 | patch edge color | black | TBD (MATLAB histogram EdgeColor default is black) | Histogram Properties → EdgeColor | TBD | |
| 56 | patch linewidth (bar edges) | 0.5 pt | TBD | Histogram → LineWidth | TBD | |
| 57 | patch force_edgecolor | True | n/a (matplotlib-specific) | n/a | 📝 NOTE | needed in matplotlib so edges aren't transparent |
| 58 | bar face color (1st color) | inherits axes color cycle (= MATLAB blue) | TBD | Histogram → FaceColor | TBD | |

---

## Section 9: Layout / Figure

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 59 | figure default size | not set (matplotlib default 6.4×4.8") | TBD (MATLAB Figure Position default) | Figure → Position | TBD | |
| 60 | figure DPI | not set (matplotlib default 100) | TBD | n/a | 📝 NOTE | DPI is display-dependent |
| 61 | subplot spacing | matplotlib tight_layout default | TBD | TBD | TBD | |

---

## Section 10: Plot type specifics

| # | Aspect | openlab-style current | MATLAB R2014b+ default | Source | Status | Notes |
|---|--------|----------------------|------------------------|--------|--------|-------|
| 62 | loglog minor grid | inherits xtick.minor.visible (True) | TBD (MATLAB default shows minor grid on log) | TBD | TBD | |
| 63 | semilogx/y minor grid | same | TBD | TBD | TBD | |
| 64 | histogram default bins | matplotlib default (auto) | TBD | Histogram → NumBins | TBD | usually explicit per call |
| 65 | imshow aspect | default (matplotlib equal) | TBD (MATLAB imagesc default) | TBD | TBD | |
| 66 | colorbar default | matplotlib default position right | TBD | Colorbar → Location | TBD | |

---

## Discrepancy summary (running tally)

Updated as rows complete. Format: row # — short description — proposed fix.

### Critical (visible at any size) — ALL FIXED in commit e4aa78a + this commit

- ✅ (row 43) `grid.linestyle: ':'` → `'-'` (fixed in e4aa78a)
- ✅ (row 45) `grid.alpha: 1.0` → `0.15` (fixed in e4aa78a)
- ✅ (row 18) `axes.titleweight: 'normal'` → `'bold'` (fixed in e4aa78a)
- ✅ (row 39) `xtick.minor.visible: True` → `False` (fixed in e4aa78a; matplotlib auto-shows on log)
- ✅ (row 8) `lines.linewidth: 1.5 → 0.5` — MATLAB Line LineWidth default is 0.5pt. We over-thickened to match matplotlib's default. Now MATLAB-correct.
- ✅ (rows 55-58) **HISTOGRAM EDGES**: `patch.edgecolor: 'black' → 'none'`, `patch.force_edgecolor: True → False`. **We had this very wrong**: MATLAB R2014b+ `histogram()` defaults to **no edges + FaceAlpha=0.6** (semi-transparent). The older `hist()` function had edges; modern `histogram()` does not. Our earlier "fidelity" attempt added edges thinking that matched MATLAB. Opposite. Now edgeless to match modern histogram().
- ✅ (row 50) `legend.edgecolor: 'black' → (0.15, 0.15, 0.15)` — MATLAB legend EdgeColor default is dark gray, not pure black.
- ✅ (row 53) `legend.fontsize: base → base * 0.9` — MATLAB auto-scales legend FontSize to 90% of axes FontSize.

### Limitations (matplotlib has no rcParam equivalent)

- 📝 (row 56) `Histogram FaceAlpha = 0.6` cannot be set via rcParams. Workaround: users call `plt.hist(data, alpha=0.6)` explicitly. Document in README.
- 📝 (row 34) `TickLength` in MATLAB is normalized (1% of axis length, ~5-7px at typical figure sizes). matplotlib uses points. Current `xtick.major.size: 5` is correct at typical figure sizes; for very small or large figures this won't auto-scale like MATLAB does. Acceptable approximation.
- 📝 (row 23) MATLAB math text uses Computer-Modern-LaTeX-like rendering for `$...$`. matplotlib defaults to a DejaVu-based mathtext. Different fonts. Approximate match requires matplotlib's `mathtext.fontset: 'cm'` but that has side effects. Leave default.

### Adjust (matters but smaller)

### Adjust (matters but smaller)

- (row 17) ⚠️ Title font size: we use `base+1` (11pt absolute). MATLAB uses `TitleFontSizeMultiplier = 1.1`, so for base 10pt MATLAB renders 11pt. Close match but **the multiplier approach is more correct**: matplotlib's `axes.titlesize: 'large'` or explicit multiplier. **Fix**: switch to `axes.titlesize` as multiplier or compute `base * 1.1`.
- (row 19) ⚠️ Label font size: same as above. MATLAB `LabelFontSizeMultiplier = 1.1`. We use `base`. **Fix**: set to `base * 1.1` (11pt for base 10pt).
- (row 46) ⚠️ MinorGridLineStyle should be `':'` (dotted) — actually this IS what we have for the main grid. After we fix #43 (main grid back to solid), we need to wire minor grid as dotted with alpha 0.25.

### Parula (separate big finding)

- (rows 10-14) ⚠️ **parula values are from pre-R2017a MATLAB**. MATLAB updated parula in R2017a ("more colorful colors and smoother transitions"). Authoritative post-R2017a 69-entry RGB data found at [tpfto.wordpress.com](https://tpfto.wordpress.com/2018/03/05/on-emulating-the-parula-colormap-in-mathematica/) — anchors (entry 1 and entry 64) match ours but middle entries diverge by ~0.01-0.05. **Fix**: replace `PARULA_DATA` with the 69-entry post-R2017a version, register as 'parula' with 69 entries.
- (row 9) 📝 R2019b+ changed default colormap size from 64 to 256 entries. Pre-R2019b is 64, R2019b+ is 256. Our 64-entry is correct for R2014b-R2019a, undersized for R2019b+. **Decision needed**: ship 64 (matches older), 256 (matches newer), or expose both via `parula_cmap(n=256)`.

### TBD (need more fetches)

- (rows 1-8) Line color RGBs — MathWorks docs don't publish exact RGB. Need authoritative third-party extraction (matlab2tikz, scientific-plot project, etc.).
- (row 28) Axes LineWidth — MATLAB doc confirms 0.5pt, ours is 0.5pt. **✅ MATCH**.
- (rows 33-37) Tick lengths — MATLAB uses normalized (1% axis length); matplotlib uses points. Need to verify what 1% of typical axis renders as in points at common figure sizes.

### Other 📝 notes

- (row 24-27) Box: MATLAB R2014b+ traditional plot defaults to Box on (full rectangle around axes). Modern R2025+ "gem" theme may differ. Our `axes.spines.*: True` matches R2014b+ traditional. **✅ MATCH**.
- The MathWorks page mentions "gem palette for light theme, glow for dark" suggesting R2025a+ has theme-based defaults. We target R2014b+ baseline, so this is out of scope.

---

## Source citations (running)

- MathWorks Axes Properties: https://www.mathworks.com/help/matlab/ref/matlab.graphics.axis.axes-properties.html — fetched 2026-06-03
- MathWorks parula: https://www.mathworks.com/help/matlab/ref/parula.html — fetched 2026-06-03 — confirms R2017a parula change + R2019b 64→256 default
- MathWorks colororder: https://www.mathworks.com/help/matlab/ref/colororder.html — fetched 2026-06-03 — note R2025a moved from "lines" to "gem" as default palette
- post-R2017a parula RGB extraction (Mathematica community): https://tpfto.wordpress.com/2018/03/05/on-emulating-the-parula-colormap-in-mathematica/ — fetched 2026-06-03 — 69-entry authoritative RGB

---

## Sources cited

- MathWorks Axes Properties: https://www.mathworks.com/help/matlab/ref/matlab.graphics.axis.axes-properties.html
- MathWorks Plot Properties / chart line: https://www.mathworks.com/help/matlab/ref/matlab.graphics.chart.primitive.line-properties.html
- MathWorks Legend Properties: https://www.mathworks.com/help/matlab/ref/matlab.graphics.illustration.legend-properties.html
- MathWorks Figure Properties: https://www.mathworks.com/help/matlab/ref/matlab.ui.figure-properties.html
- MathWorks Histogram Properties: https://www.mathworks.com/help/matlab/ref/matlab.graphics.chart.primitive.histogram-properties.html
- MathWorks colororder: https://www.mathworks.com/help/matlab/ref/colororder.html
- MathWorks parula colormap: https://www.mathworks.com/help/matlab/ref/parula.html

(More sources added as cited.)
