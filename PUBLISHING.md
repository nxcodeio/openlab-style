# Publishing openlab-style to PyPI

This runbook ships the package to PyPI so `pip install openlab-style` works globally.

**You need to do**: register PyPI account + get an API token (10 min, identity-bound, can't be delegated).
**Everything else is automated.** The wheel + sdist are already built in `dist/`.

---

## TL;DR

```bash
# After you have a PyPI API token in ~/.pypirc (see below):
cd ~/projects/openlab-style

# Step 1: upload to TestPyPI (rehearsal)
.venv/bin/twine upload --repository testpypi dist/*

# Step 2: verify on test.pypi.org, then upload to real PyPI
.venv/bin/twine upload dist/*

# Step 3: tag the release in git
git tag v0.1.0
git push origin v0.1.0
```

---

## One-time setup (10 min)

### 1. Create PyPI account

Go to https://pypi.org/account/register/

- Email: `zirongch@umich.edu` (matches pyproject.toml; can change later)
- Username: pick something — `vivianchi` or `nxcodeio` likely available
- Strong password
- **MFA is required** — enable either TOTP (Authy / 1Password) or a hardware key (recommended if you have one)

### 2. Create TestPyPI account (recommended — separate from real PyPI)

Same flow at https://test.pypi.org/account/register/

TestPyPI is a sandbox. You upload there first, install from there, verify it works, *then* push to real PyPI. This catches metadata bugs before they hit the permanent record.

### 3. Generate API tokens

PyPI no longer accepts passwords for uploads. You need scoped API tokens.

**Real PyPI:**
- Log in to pypi.org
- Account settings → API tokens → Add API token
- Token name: `openlab-style-publish` (or whatever)
- Scope: **Project: openlab-style** (you'll only be able to scope to project after the first upload — for the very first upload, use scope "Entire account" and rotate to project-scoped right after)
- Copy the token (starts with `pypi-...`) immediately — you won't see it again

**TestPyPI** (same flow on test.pypi.org):
- Generates a separate token, starts with `pypi-...` too

### 4. Configure twine

Create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...YOUR-REAL-PYPI-TOKEN...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIdGVzdC5weXBp...YOUR-TESTPYPI-TOKEN...
```

`chmod 600 ~/.pypirc` (twine warns if it's world-readable).

**Alternative**: don't store the token, paste it interactively each time twine prompts. Safer but slower.

---

## Publish flow

### Pre-flight (already done, but verify)

```bash
cd ~/projects/openlab-style

# Tests still pass?
.venv/bin/pytest tests/ -q
# Expected: 8 passed

# Build artifacts present?
ls dist/
# Expected: openlab_style-0.1.0-py3-none-any.whl  openlab_style-0.1.0.tar.gz

# Metadata still valid?
.venv/bin/twine check dist/*
# Expected: PASSED for both
```

If anything fails, fix before uploading. **PyPI versions are immutable** — you cannot re-upload `0.1.0` after publishing it. If you push a broken `0.1.0`, the only fix is to publish `0.1.1`.

### Step 1: Upload to TestPyPI

```bash
.venv/bin/twine upload --repository testpypi dist/*
```

Expected output: URLs like `https://test.pypi.org/project/openlab-style/0.1.0/`. Open it. Verify:
- Description renders correctly (the README on the page should look right)
- Classifiers listed
- License is MIT
- Project URLs go to GitHub

### Step 2: Verify TestPyPI install works

```bash
# Fresh venv to be sure
rm -rf /tmp/test-pypi-install
python3 -m venv /tmp/test-pypi-install
/tmp/test-pypi-install/bin/pip install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    openlab-style

# The --extra-index-url is critical: TestPyPI has no matplotlib, so pip needs
# to fetch matplotlib from real PyPI while fetching openlab-style from TestPyPI.

/tmp/test-pypi-install/bin/python -c "
import openlab_style
openlab_style.apply()
print('TestPyPI install: OK, version', openlab_style.__version__)
"

rm -rf /tmp/test-pypi-install
```

If you see `TestPyPI install: OK, version 0.1.0` → all green, proceed to real PyPI.
If anything errors → debug, bump version to `0.1.1`, rebuild, re-upload to TestPyPI.

### Step 3: Upload to real PyPI

```bash
.venv/bin/twine upload dist/*
```

This pushes `openlab_style-0.1.0-py3-none-any.whl` + `openlab_style-0.1.0.tar.gz` to pypi.org. Within ~1 minute, `pip install openlab-style` will work worldwide.

Verify (from any machine, any clean Python env):

```bash
pip install openlab-style
python -c "import openlab_style; openlab_style.apply(); print('LIVE on PyPI')"
```

### Step 4: Tag the release in git

```bash
git tag -a v0.1.0 -m "openlab-style 0.1.0 — initial PyPI release"
git push origin v0.1.0
```

Then on GitHub: https://github.com/nxcodeio/openlab-style/releases → "Draft a new release" → pick tag `v0.1.0` → paste release notes (one-liner OK: "Initial release. See README for usage."). Optional but nice.

---

## Cutting future releases

For `0.1.1` / `0.2.0` / etc:

1. Bump version in `pyproject.toml` (`version = "0.1.1"`) and in `src/openlab_style/__init__.py` (`__version__ = "0.1.1"`)
2. Update CHANGELOG (when we have one)
3. `rm -rf dist/ build/ src/*.egg-info`  (clean old artifacts)
4. `.venv/bin/python -m build`
5. `.venv/bin/twine check dist/*`
6. `.venv/bin/twine upload --repository testpypi dist/*` (rehearse)
7. `.venv/bin/twine upload dist/*` (ship)
8. `git tag v0.1.1 && git push origin v0.1.1`

Eventually automate via GitHub Actions → publish on tag push using OIDC trusted publishing (no token in CI). Worth doing once we have 2-3 releases.

---

## Notes

- **PyPI name normalization**: `openlab-style` and `openlab_style` are the same package on PyPI. Both `pip install openlab-style` and `pip install openlab_style` resolve to ours.
- **Name collision**: someone owns `openlab` on PyPI (NORCE's OpenLab Drilling client, unrelated). Doesn't block us — different name. May want to call out in README in future: "Not affiliated with OpenLab Drilling."
- **Wheel is universal**: `py3-none-any` — works on any Python ≥3.9, any OS, any arch. Pure Python, no compiled extensions.
- **Size**: ~8 KB. Tiny.
