# Welcome to PyDREAM's documentation!

A Python implementation of the MT-DREAM(ZS) algorithm presented in [Laloy and Vrugt 2012](http://faculty.sites.uci.edu/jasper/files/2016/04/72.pdf).

PyDREAM is a focused Bayesian sampling library designed for expensive black-box likelihoods and simulator-based inference workflows, particularly:

* ODE and dynamical systems models
* systems biology workflows
* non-differentiable or numerically unstable likelihoods
* multimodal posterior distributions
* models where gradient-based approaches are difficult or impractical

PyDREAM is not intended to compete with probabilistic programming frameworks such as Stan or PyMC. Instead, it focuses on robust differential-evolution MCMC sampling for scientific models where gradient-based inference is difficult, unreliable, or unavailable.

**Quickstart:** The main function to run DREAM is in {py:func}`pydream.core.run_dream`.

This provides reasonable defaults, but a variety of options are available for customizing DREAM.
These can be passed as keyword arguments to {py:func}`pydream.core.run_dream`. See the {py:class}`pydream.Dream.Dream` class for a list of options.

Examples are available in the examples directory of the GitHub repo.

```{toctree}
:maxdepth: 4
:caption: Contents:

Installation <installation>
Module Reference <pydream>
```

# Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`