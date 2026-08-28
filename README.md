# MTI-EXTENSIONS

This repository contains the companion manuscript for mean-tilted interval
regression and dynamic endpoint models. The paper develops generalized-Bayes
computation for fixed-content endpoint targets after the interval target has
been specified.

The companion tolerance paper remains in `AntonioAPDL/RQR-GIBBS`. That paper
develops the fixed-content geometry, the mean-preserving interval, the
mean-tilted interval family, the TCSP tolerance action, and the iid tolerance
validation. This repository focuses on endpoint regression, deterministic
feature readouts, dynamic endpoint models, Gibbs computation, ECM mode
calculation, and diagnostic requirements.

## Files

- `main.tex`: main companion article.
- `mti-extensions-supplement.tex`: derivations and computational details.
- `refs.bib`: bibliography shared with the tolerance paper.
- `STYLE_PROFILE.md`: academic writing guidelines used for manuscript edits.
- `Makefile`: reproducible local build targets.

## Build

```bash
make pdf
make supplement
make all
```

Generated PDFs and TeX auxiliary files are ignored.
