# Production changelog - 2026-10-07

- Adopted the title **Population readout can hide state perturbations in
  critical nonlinear quantum search** in the release documentation.
- Split the monolithic figure generator into four standalone scripts, each
  containing its complete all-panels plot and writing exactly one vector PDF.
- Moved the unchanged analytical and ODE routines into `src/numerics.py`, with
  common styling and PDF output in `src/plotting.py`. Preserved all plotted
  parameters, integration settings, figure labels, and appearance.
- Kept all reproduction calculations in memory. Disabled bytecode output and
  placed Matplotlib caches in automatically removed temporary directories.
- Included pinned dependencies, portable instructions, final figures, and
  unchanged supporting numerical arrays and the original convergence record.
- Paired this code archive with a separate self-contained Overleaf project and
  compiled manuscript. The manuscript production changes are its new title,
  Pi_m/calligraphic C_N notation, finite-N abstract precision, exact supplied
  acknowledgments, and an explicit data-availability link placeholder.
- No new models, numerical experiments, derivation audit, bibliography audit,
  external publication, or license grant were introduced.
