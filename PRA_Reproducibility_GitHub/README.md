# Population readout can hide state perturbations in critical nonlinear quantum search

Self-contained reproduction files for the manuscript's four figures. No
notebook, LaTeX installation, network access at runtime, or legacy project is
needed. Figure 1 is a deterministic Matplotlib construction, not TikZ or
generative-AI artwork.

## Setup

Tested with Python 3.13.14 and the pinned versions in `requirements.txt`.
From the extracted repository root:

```sh
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```sh
source .venv/bin/activate
```

Then install dependencies:

```sh
python -m pip install -r requirements.txt
```

## Generate one complete figure

Each command independently generates all panels of one manuscript figure:

```sh
python scripts/fig01_phase_shear.py
python scripts/fig02_gp_branches.py
python scripts/fig03_gp_perturbation.py
python scripts/fig04_quintic.py
```

| Script | Only persistent output |
|---|---|
| `scripts/fig01_phase_shear.py` | `figures/fig1_tangent_shear.pdf` |
| `scripts/fig02_gp_branches.py` | `figures/fig2_branch_functions.pdf` |
| `scripts/fig03_gp_perturbation.py` | `figures/fig3_nonlinear_example.pdf` |
| `scripts/fig04_quintic.py` | `figures/fig4_quintic.pdf` |

Outputs are resolved relative to each script's repository, not the shell's
current directory. Commands may overwrite their corresponding supplied PDF.
They do not write arrays, CSVs, logs, intermediate images, or Python bytecode.
Matplotlib's font cache is placed in a temporary directory and removed on exit.
No convergence campaign is launched by these commands.

## Structure and preserved settings

- `scripts/`: one complete figure-generation source per figure.
- `src/numerics.py`: shared analytical curves and the original first-order and
  nonlinear ODE implementations; no file-writing side effects.
- `src/plotting.py`: shared publication style and final-PDF saving.
- `figures/`: the four final vector PDFs, also included in the Overleaf package.
- `data/`: unchanged original supporting arrays and convergence record. These
  are reference material, not runtime inputs or script-generated outputs.

Figures 2 and 4 recompute their plotted finite-size markers using DOP853 with
relative tolerance `2e-10` and absolute tolerance `2e-13`, initial tangent
`(0, 1)`, `k=1`, and `g=(N-1)/sqrt(N)`. The thresholds are
`epsilon=[0.05, 0.1, 0.2, 0.3]`; analytic curves use 401 points from 0.04 to 0.35.
GP sizes are `1e4, 1e8`; quintic sizes are `1e6, 1e10`.

Figure 3 uses the established `N=256`, `eta=5e-4` pulse trajectory and separate
tangent comparison, DOP853 relative/absolute tolerances `2e-12`/`2e-14`, and
maximum clock step `0.012`. The original shared routine retains the half-pulse
calculation used in the existing error report, in memory only. No refined
tolerance sweep is run. The pulse is supported on clock interval `(0.12, 0.35)`.

`data/branch_functions.npz` contains the plotted analytic/finite-size values and
tangent components. `data/nonlinear_example.npz` contains sampled populations,
distances, tangent predictions, and normalized complex trajectories.
`data/verification.json` is the original archived convergence record, not a new
scientific audit. The reproduction check compares regenerated figures and
numerical values against these established files.

## Publication

This is a local, GitHub-ready package; the author will choose the destination
and publish it. No repository URL, DOI, or license grant has been assigned.
After publication, replace the manuscript's Data availability placeholder with
the real permanent link. `CHANGELOG.md` describes the production refactor.
