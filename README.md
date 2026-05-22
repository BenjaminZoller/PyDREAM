# PyDREAM

A Python implementation of the MT-DREAM(ZS) algorithm presented in [Laloy and Vrugt 2012](http://faculty.sites.uci.edu/jasper/files/2016/04/72.pdf).

## Authorship and Maintenance

PyDREAM was originally developed by Erin Shockley, Ortega, and other contributors.
It is currently maintained and being modernized by Benjamin Zoller, with AI assistance from Google's Gemini.

For example usage, see the `examples` folder. Two of the examples, CORM and Robertson, require the Python modeling framework PySB.

Documentation is available at Read the Docs.

## Installation for Development

To install PyDREAM locally in editable mode along with its testing dependencies, run the following from the root of the repository:

```bash
pip install -e .[test]
```

## Testing

PyDREAM uses `pytest` for unit testing. After installing the test dependencies, you can run the entire test suite simply by running:

```bash
pytest
```

To run the tests with code coverage reporting:

```bash
pytest --cov
```

## Building and Deployment

PyDREAM uses modern `pyproject.toml` packaging. To build the distribution archives (wheel and source distribution) and upload them to PyPI, use `build` and `twine`:

```bash
pip install build twine
python -m build
python -m twine upload dist/*
```