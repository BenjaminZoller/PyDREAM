# PyDREAM

A Python implementation of the MT-DREAM(ZS) algorithm presented in [Laloy and Vrugt 2012](http://faculty.sites.uci.edu/jasper/files/2016/04/72.pdf).

PyDREAM is a focused Bayesian sampling library designed for expensive black-box likelihoods and simulator-based inference workflows, particularly:

* ODE and dynamical systems models
* systems biology workflows
* non-differentiable or numerically unstable likelihoods
* multimodal posterior distributions
* models where gradient-based approaches are difficult or impractical

PyDREAM is not intended to compete with probabilistic programming frameworks such as Stan or PyMC. Instead, it focuses on robust differential-evolution MCMC sampling for scientific models where gradient-based inference is difficult, unreliable, or unavailable.

## Authorship and Maintenance

PyDREAM was originally developed by Erin Shockley, Oscar Ortega, and other contributors.

The project is currently maintained and modernized by Benjamin Zoller.

## Documentation and Examples

Example workflows are available in the `examples` folder.

Some examples, including CORM and Robertson, require the systems biology framework PySB.

Documentation is available on Read the Docs.

## Installation for Development

Install PyDREAM in editable mode with test dependencies:

```bash
pip install -e ".[test]"
```

## Testing

PyDREAM uses `pytest` for testing.

Run the full test suite:

```bash
pytest -vs
```

Run tests with coverage:

```bash
pytest --cov
```

## Building and Deployment

PyDREAM uses modern `pyproject.toml` packaging.

Build source and wheel distributions:

```bash
pip install build twine
python -m build
```

Upload distributions to PyPI:

```bash
python -m twine upload dist/*
```

## Building the Documentation

To build the HTML documentation locally:

```bash
pip install -e ".[docs]"
cd docs
make html
