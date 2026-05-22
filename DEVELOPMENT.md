# DEVELOPMENT.md

## Project Goals

This project is a maintained continuation/fork of PyDREAM focused on:

* Compatibility with modern Python and scientific Python ecosystems
* Reliability and reproducibility
* Improved testing and CI
* Better typing, linting, and code quality
* Long-term maintainability of a scientific MCMC codebase

The project targets:

* Python >= 3.11
* Modern NumPy/SciPy/PySB ecosystems
* Cross-platform compatibility (Linux/macOS/Windows)

---

# Maintenance Philosophy

Scientific software must prioritize:

1. Correctness
2. Stability
3. Numerical robustness
4. Maintainability

Style and linting are important, but statistical correctness and regression protection take precedence.

---

# Supported Versions

## Python

Supported Python versions:

* 3.11
* 3.12
* 3.13

Python versions older than 3.11 are not supported.

## Dependencies

General policy:

* Avoid overly strict upper bounds
* Pin minimum supported versions
* Regularly test against newest releases

---

# Development Standards

## Formatting and Linting

The project uses:

* `ruff` for linting and formatting
* `pyright`/Pylance-compatible typing
* `pytest` for testing

All pull requests must pass linting and typing checks.

## Type Hints

Type hints should be added progressively.

Priority areas:

1. Public APIs
2. Sampling interfaces
3. Probability/log-likelihood interfaces
4. Array-returning functions
5. Configuration structures

Use:

* `numpy.typing.NDArray`
* explicit return types
* explicit Optional/Union typing

Full strict typing is not required initially.

---

# Testing Strategy

## General Philosophy

MCMC algorithms are stochastic and may behave differently across:

* operating systems
* NumPy versions
* BLAS implementations
* CPU architectures

Tests should therefore validate statistical correctness and invariants rather than exact sample sequences.

---

## Test Categories

### Unit Tests

Fast deterministic tests validating:

* shapes
* return types
* boundary conditions
* exceptions
* serialization/restart behavior
* API consistency

---

### Statistical Tests

Statistical tests validate sampler behavior on simple known targets.

Recommended targets:

* standard Gaussian
* correlated Gaussian
* bounded distributions
* simple multimodal distributions

Assertions should use tolerant statistical bounds rather than exact equality.

Example checks:

* posterior mean approximately correct
* covariance approximately correct
* finite log probabilities
* reasonable acceptance rates
* convergence sanity checks

Example:

```python id="u3q0ya"
assert np.allclose(mean, expected_mean, atol=0.15)
```

Prefer validating statistical summaries over exact reproducibility of chains.

---

### Smoke Tests

Ensure:

* samplers execute successfully
* multiprocessing works
* chains complete without crashes
* restart functionality works

Slow statistical tests may be marked separately.

Example:

```python id="6j6r4l"
@pytest.mark.slow
```

---

# Continuous Integration

CI should test:

* Linux
* macOS
* Windows

Against:

* Python 3.11
* Python 3.12
* Python 3.13

CI should include:

* linting
* typing
* unit tests
* statistical tests
* packaging validation

---

# Packaging

The project should use modern packaging standards.

Requirements:

* `pyproject.toml`
* wheel builds
* source distributions

Recommended structure:

```text id="t4t6jx"
src/
tests/
docs/
```

---

# API Stability

Public APIs should remain stable whenever practical.

Breaking changes require:

* changelog entry
* migration guidance
* semantic version increment

Deprecated APIs should emit warnings before removal.

---

# Numerical Robustness

Code should:

* avoid hidden dtype conversions
* avoid unnecessary global RNG usage
* validate array shapes explicitly
* handle NaN/inf robustly
* fail loudly on invalid probability calculations

---

# Pull Request Guidelines

PRs should:

* include tests for bug fixes
* avoid unrelated formatting churn
* preserve backward compatibility where possible
* include concise rationale in commit messages

Large refactors should be split into smaller reviewable commits.

---

# Documentation Priorities

Important documentation areas:

1. sampler behavior
2. restart/checkpoint semantics
3. multiprocessing behavior
4. convergence diagnostics
5. compatibility matrix

Examples should be executable and tested where practical.

---

# Long-Term Goals

Potential future improvements:

* stricter typing
* benchmark suite
* performance profiling
* improved diagnostics
* modern RNG architecture
* better parallel execution abstractions

These goals should not compromise correctness or maintainability.
