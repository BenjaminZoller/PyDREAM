# GEMINI.md

# PyDREAM Agent Directives

## Objective

Modernize and maintain the `pydream` codebase for:

* Python >= 3.11
* NumPy >= 2.x
* modern scientific Python tooling
* improved maintainability and code quality

while preserving the original DREAM sampling behavior and statistical semantics.

---

# Core Constraints

## 1. Preserve Mathematical Semantics

The DREAM sampling algorithm and its statistical behavior must remain unchanged.

Do NOT introduce changes that alter:

* proposal generation
* acceptance logic
* convergence behavior
* chain evolution
* probability calculations
* multiprocessing sampling semantics

Performance improvements and refactoring are acceptable only if statistical behavior remains equivalent.

---

## 2. Prefer Minimal, Targeted Changes

Prefer:

* localized fixes
* incremental refactors
* explicit code changes
* backwards-compatible improvements

Avoid:

* unnecessary rewrites
* broad architectural refactors
* stylistic churn unrelated to the task

---

## 3. Modern Python Compatibility

The codebase targets:

* Python 3.11+
* NumPy 2.x+

Remove obsolete compatibility code for:

* Python 2.x
* deprecated NumPy aliases
* legacy multiprocessing patterns

---

## 4. Maintain Scientific Robustness

Scientific correctness takes precedence over stylistic preferences.

When modifying stochastic or numerical code:

* preserve numerical stability
* avoid hidden dtype changes
* preserve array shape semantics
* avoid introducing nondeterministic multiprocessing bugs

---

# Modernization Guidelines

## NumPy 2.x Compatibility

Replace deprecated aliases:

* `np.float` → `float` or `np.float64`
* `np.int` → `int` or explicit integer dtype
* `np.bool` → `bool`
* `np.object` → `object`

Verify:

* boolean masking behavior
* broadcasting semantics
* `np.frombuffer` shared-memory usage
* `np.nan_to_num` compatibility
* `np.linalg` API usage

---

## Python 3.11+ Compatibility

Modernize:

* multiprocessing context handling
* process spawning behavior
* daemon process interactions
* outdated unittest compatibility code

Remove:

* Python 2 conditionals
* obsolete fallback logic
* dead compatibility branches

---

## Typing and Linting

Use:

* `ruff`
* PEP-8 compliant formatting
* modern type hints
* `numpy.typing` where appropriate

Prioritize type hints for:

* public APIs
* sampling interfaces
* probability/log-likelihood functions

Resolve:

* unused imports
* unreachable code
* undefined variables
* unsafe Optional handling

Avoid excessive typing complexity.

---

# Testing Requirements

## General Principles

MCMC behavior is stochastic and platform-dependent.

Do NOT rely on exact chain reproducibility across systems.

Prefer tests validating:

* statistical invariants
* finite outputs
* expected shapes
* approximate posterior statistics
* restart/resume correctness
* multiprocessing stability

---

## Preferred Test Types

### Unit Tests

Validate:

* API behavior
* shapes and dtypes
* edge cases
* serialization
* restart logic

### Statistical Tests

Use simple known targets:

* Gaussian distributions
* correlated Gaussian targets
* bounded distributions

Validate:

* approximate posterior mean/covariance
* finite log probabilities
* reasonable acceptance rates

Use tolerant thresholds.

---

# Workflow Instructions

When implementing fixes:

1. Focus on one module or issue at a time.
2. First identify the root cause before modifying code.
3. Prefer minimal diffs.
4. Add or update tests for bug fixes.
5. Verify compatibility with:

   * Python 3.11+
   * NumPy 2.x+
6. Ensure all changes respect the Core Constraints.

When possible, provide:

* unified diffs
* concise rationale for changes
* notes about numerical or compatibility implications

---

# Existing Bug Documentation

Known historical bugs and fixes are documented in:

```text id="4p6k6r"
PYDREAM_BUGS_DOCUMENTATION.md
```

Preserve existing fixes and avoid reintroducing known regressions.
