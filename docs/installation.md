# Installing PyDREAM

PyDREAM can be installed from the Python Package Index using `pip`:

```bash
pip install pydream
```

## Requirements

PyDREAM requires `numpy` and `scipy` (and Python >= 3.11), which will be installed automatically with PyDREAM when using `pip`.

## Installation for Development

Install PyDREAM in editable mode with test dependencies:

```bash
pip install -e ".[test]"
```

## Testing

PyDREAM uses `pytest` for testing. Run the full test suite:

```bash
pytest -vs
```

Run tests with coverage:

```bash
pytest --cov
```