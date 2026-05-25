# GEMINI.md

# PyDREAM Agent Directives

## Objective

Maintain and modernize `pydream` for:

* Python >= 3.11
* NumPy >= 2.x
* modern scientific Python tooling

while preserving:

* DREAM sampling behavior
* statistical semantics
* public API compatibility unless explicitly requested otherwise

---

# Core Constraints

## 1. Preserve Scientific Behavior

Do NOT alter:

* proposal generation
* acceptance logic
* convergence behavior
* chain evolution semantics
* probability calculations
* multiprocessing sampling semantics

Refactoring and optimization are acceptable only if statistical behavior remains equivalent.

---

## 2. Prefer Minimal, Localized Changes

Prefer:

* incremental refactors
* localized fixes
* backward-compatible improvements
* explicit validation and error handling

Avoid:

* unnecessary rewrites
* broad architectural refactors
* stylistic churn unrelated to the task

---

## 3. Maintain Numerical Robustness

When modifying numerical or stochastic code:

* preserve array shape semantics
* avoid hidden dtype changes
* avoid unnecessary global RNG usage
* preserve multiprocessing safety
* fail loudly on invalid numerical states

Scientific correctness takes precedence over stylistic preferences.

---

# Compatibility Requirements

## Python

Target:

* Python 3.11+
* modern multiprocessing behavior

Remove:

* Python 2 compatibility code
* obsolete fallback branches
* outdated unittest compatibility logic

## NumPy

Target:

* NumPy 2.x+

Replace deprecated aliases:

* `np.float`
* `np.int`
* `np.bool`
* `np.object`

Verify:

* broadcasting behavior
* boolean masking behavior
* shared-memory array handling
* `np.linalg` compatibility
* `np.nan_to_num` behavior

---

# Typing and Linting

Use:

* `ruff`
* PEP-8 compliant formatting
* modern type hints
* `numpy.typing` where appropriate

Prioritize typing for:

* public APIs
* sampler interfaces
* probability/log-likelihood functions
* config/result/state objects

Resolve:

* unused imports
* unreachable code
* undefined variables

Avoid excessive typing complexity.

---

# Testing Requirements

MCMC behavior is stochastic and platform-dependent.

Do NOT rely on exact chain reproducibility across systems.

Prefer tests validating:

* finite outputs
* expected shapes and dtypes
* approximate posterior statistics
* reasonable acceptance rates
* restart/resume correctness
* multiprocessing stability

Recommended statistical targets:

* standard Gaussian
* correlated Gaussian
* bounded distributions
* simple multimodal targets

Use tolerant statistical thresholds.

---

# Workflow Instructions

When implementing changes:

1. Identify the root cause first.
2. Prefer minimal diffs.
3. Focus on one issue or module at a time.
4. Add or update tests for bug fixes.
5. Preserve backward compatibility unless explicitly instructed otherwise.
6. Verify compatibility with Python 3.11+ and NumPy 2.x+.

When possible, provide:

* unified diffs
* concise rationale for changes
* notes about numerical or compatibility implications

---

# Existing Bug Documentation

Known historical bugs and fixes are documented in:

```text id="0qlm1p"
PYDREAM_BUGS_DOCUMENTATION.md
```

Preserve existing fixes and avoid reintroducing known regressions.
