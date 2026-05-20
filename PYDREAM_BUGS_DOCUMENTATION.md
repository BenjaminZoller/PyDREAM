# PyDream Diagnostics and Known Bugs

This document outlines two critical bugs and architectural flaws identified in the `pydream` package (specifically related to the implementation of Multiple-Try Metropolis, or `multitry`, when combined with multiprocessing). 

These issues severely impact performance and stability when evaluating models with complex likelihood functions.

---

## Bug 1: The `multitry=2` Crash (NumPy Dimensionality Squeeze)

### Symptom
When running `pydream` with `multitry=2` and `parallel=True`, the execution immediately crashes inside the parallel worker pool with the following traceback:

```python
TypeError: object of type 'numpy.float64' has no len()
```

### Root Cause
This is a classic NumPy dimensionality bug triggered by how `pydream` generates and maps alternative proposal points in Differential Evolution.

When `multitry=X` is enabled, PyDream generates `X-1` alternative proposal points to evaluate simultaneously. 
1. If `multitry=5`, PyDream generates 4 alternative points, resulting in a 2D NumPy array of shape `(4, N_parameters)`.
2. When PyDream passes this 2D array to `multiprocessing.Pool.map()`, the mapping function iterates over the first axis (rows), correctly handing a 1D array of `N_parameters` to the likelihood function 4 times.
3. **However, if `multitry=2`**, PyDream generates exactly **1** alternative point. Due to NumPy's default array squeezing behavior (or lack of strict reshaping), the array collapses from a 2D shape of `(1, N_parameters)` down to a 1D shape of `(N_parameters,)`.
4. When this 1D array is passed to `pool.map()`, Python's `map` iterates over the elements of the 1D array itself. It spawns `N_parameters` parallel jobs, passing a single scalar (`numpy.float64`) to the likelihood function instead of the full parameter array. 

The user's likelihood function expects an array of parameters but receives a single float, causing an immediate crash when it attempts to call `len()` or unpack it.

### How to Fix in Fork
Inside PyDream's source code (likely near the `mt_evaluate_logps` function or where the reference points are generated in `Dream.py`), explicitly enforce a 2D shape for the `reference_pts` array before passing it to `pool.map`. 

```python
# Example pseudo-fix
if reference_pts.ndim == 1:
    reference_pts = reference_pts.reshape(1, -1)
```

---

## Bug 2: The Nested Multiprocessing Bottleneck (`multitry` + `parallel=True`)

### Symptom
When running `pydream` with `parallel=True` and any valid `multitry > 2` (e.g., `multitry=5`), the CPU usage instantly saturates to 100%, but the iteration speed slows to a crawl (sluggish/frozen performance).

### Root Cause
This is caused by a catastrophic Inter-Process Communication (IPC) bottleneck due to **Nested Multiprocessing**.

In PyDream, the primary MCMC loop spawns parallel workers based on the number of chains (e.g., 12 chains = 12 workers). However, PyDream carelessly passes the exact same `parallel=True` flag down into the internal stepper function used for `multitry`:

```python
# Inside pydream/Dream.py

# 1. The Main PyDream Process maps the chains:
pool.map(_sample_dream, args) 

# 2. Inside the worker running a specific chain, the multi-try function is called:
self.mt_evaluate_logps(self.parallel, self.multitry, ...)

# 3. Inside mt_evaluate_logps, another pool is spawned/mapped:
logps = p.map(call_logp, args) 
```

Because `self.parallel` is still `True` inside the worker, **each of the 12 chain workers spawns its own sub-pool of workers** to evaluate the `multitry` candidates. 

If your likelihood function relies on complex objects (e.g., PySB models, Cython-compiled ODE solvers, large datasets), Python's multiprocessing must serialize (pickle) all of these objects to pass them to the sub-workers. The time required to pickle and unpickle the environment entirely eclipses the actual ODE math computation. The CPU spends 99% of its cycles on IPC overhead and context-switching (Thread Thrashing).

### How to Fix in Fork
PyDream needs to separate the parallelization of the *chains* from the parallelization of the *multitry evaluations*. 

1. **Option A:** Prevent nested pools entirely. If the chains are already running in a `Pool`, force `mt_evaluate_logps` to evaluate its proposals sequentially using a standard list comprehension or `map()` instead of a `multiprocessing.Pool`.
2. **Option B:** Allow the user to specify `parallel_chains=True` and `parallel_multitry=False` at the API level so they can manually control where the multiprocessing boundary occurs.

### Workarounds (Without Forking)
1. Set `multitry=False` to completely avoid the nested loop.
2. To compensate for the loss of `multitry` tunneling, rely on Differential Evolution's intrinsic mixing mechanics by setting `gamma_levels=6` and `nCR=10` in `run_dream()`.
3. Restrict underlying C-level threads to prevent thread thrashing when multiprocessing is active:

```python
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
```