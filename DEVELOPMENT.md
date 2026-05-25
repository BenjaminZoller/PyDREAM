# DEVELOPMENT.md

## Project Goals

PyDREAM is a maintained continuation of the original project focused on:

* compatibility with modern Python and scientific Python ecosystems
* reliability and numerical robustness
* improved testing and CI
* better typing, linting, and maintainability
* preserving the original DREAM sampling behavior and API

The project targets:

* Python >= 3.11
* modern NumPy/SciPy/PySB ecosystems
* cross-platform compatibility (Linux/macOS/Windows)

PyDREAM remains a focused black-box Bayesian sampler intended for:

* expensive likelihoods
* simulator-based and ODE models
* systems biology workflows
* non-gradient-friendly inference
* multimodal or difficult posterior landscapes

It is not intended to become a full probabilistic programming framework.

---

# History and Authorship

PyDREAM was originally authored by Erin Shockley, Oscar Ortega, and previous contributors.

The project is currently maintained by **Benjamin Zoller**, who is leading the modernization, compatibility, and maintenance effort.

---

# Maintenance Philosophy

Scientific software must prioritize:

1. correctness
2. stability
3. numerical robustness
4. maintainability

Statistical correctness and regression protection take precedence over stylistic refactoring.

The DREAM algorithm and its statistical behavior should remain unchanged unless fixing a verified bug.

Avoid altering:

* proposal generation
* acceptance logic
* convergence behavior
* chain evolution semantics

Modernization should focus primarily on tooling, testing, maintainability, and internal structure around the sampler core.

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

* avoid overly strict upper bounds
* pin minimum supported versions
* regularly test against newest releases

---

# Development Standards

## Tooling

The project uses:

* `ruff` for linting and formatting
* `pyright`/Pylance-compatible typing
* `pytest` for testing

All pull requests should pass linting, typing, and test checks.

## Type Hints

Type hints should be introduced progressively.

Priority areas:

1. public APIs
2. sampling interfaces
3. probability/log-likelihood interfaces
4. configuration objects
5. result/state objects

Use:

* `numpy.typing.NDArray`
* explicit return types
* explicit Optional/Union typing

Avoid excessive typing complexity.

---

# Testing Strategy

## General Philosophy

MCMC algorithms are stochastic and may behave differently across:

* operating systems
* NumPy versions
* BLAS implementations
* CPU architectures

Tests should validate statistical correctness and invariants rather than exact sample reproducibility.

## Unit Tests

Fast deterministic tests validating:

* shapes and dtypes
* return values
* edge cases and exceptions
* restart/checkpoint behavior
* multiprocessing stability
* API consistency

## Statistical Tests

Statistical tests should use simple known targets:

* standard Gaussian
* correlated Gaussian
* bounded distributions
* simple multimodal targets

Focus on validating:

* finite outputs
* approximate posterior summaries
* reasonable acceptance rates
* convergence sanity checks

Prefer tolerant statistical assertions over exact equality.

## Smoke Tests

Ensure:

* samplers execute successfully
* multiprocessing works
* chains complete without crashes

Slow statistical tests may be marked separately.

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

The project uses modern Python packaging standards.

Requirements:

* `pyproject.toml`
* wheel builds
* source distributions

Recommended structure:

```text id="f07yui"
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

# Modernization Roadmap

## 1. Input Validation and Internal Config Object

Introduce centralized validation and structured configuration handling.

Goals:

* reduce fragile keyword handling
* normalize user inputs early
* improve error messages
* preserve backward compatibility

Possible direction:

```python id="z7gnz6"
@dataclass(frozen=True)
class DreamConfig:
    n_chains: int
    n_iterations: int
    n_params: int
    multitry: int
```

---

## 2. Result Object While Preserving Legacy Output

Introduce a structured result container while preserving the original return format.

Possible direction:

```python id="1a07b7"
@dataclass
class DreamResult:
    sampled_params: np.ndarray
    log_ps: np.ndarray
    acceptance_rates: np.ndarray
    metadata: dict
```

Potential future methods:

```python id="ofavb0"
result.summary()
result.save()
result.to_inference_data()
```

---

## 3. Internal Sampler State Object

Replace loosely coupled internal arrays with explicit sampler state handling.

Possible direction:

```python id="6lny9v"
@dataclass
class DreamState:
    chains: np.ndarray
    log_probs: np.ndarray
    accepted: np.ndarray
    iteration: int
```

Goals:

* improve maintainability
* simplify debugging
* reduce race-condition risks
* improve restart/checkpoint handling

---

## 4. Statistical Regression Tests

Strengthen regression protection without relying on exact chain reproducibility.

Focus on:

* approximate posterior statistics
* restart behavior
* multiprocessing stability
* finite outputs
* valid acceptance rates

---

## 5. ArviZ Integration

Expose PyDREAM outputs to the modern Bayesian diagnostics ecosystem.

Possible direction:

```python id="0hm55l"
result.to_inference_data()
```

ArviZ integration should remain optional.

---

## 6. RNG Modernization

Move progressively toward modern NumPy RNG handling.

Potential direction:

* support `numpy.random.Generator`
* reduce hidden global RNG usage
* preserve statistical behavior

This should happen only after regression tests are sufficiently strong.

---

## 7. Parallel Executor Abstraction

Separate multiprocessing management from sampling logic.

Possible direction:

```python id="xmv1ew"
class Executor:
    def map(self, fn, items):
        ...
```

Goals:

* improve multiprocessing reliability
* isolate execution backends
* simplify debugging

---

## 8. Performance Benchmarks and Selective Optimization

Optimize only after correctness and maintainability are stable.

Potential areas:

* array allocation patterns
* proposal-generation overhead
* multiprocessing bottlenecks
* unnecessary array copies

Benchmark before optimizing.

Avoid premature micro-optimizations.

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

# Long-Term Notes

Potential future directions include:

* stricter typing
* benchmark suites
* improved diagnostics
* modular proposal kernels
* improved checkpointing
* mixed discrete/continuous parameters
* experimental model-selection extensions

These goals should not compromise correctness or maintainability.
