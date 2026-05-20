# Gemini Code Assist Agent Directives: PyDream Modernization & Bug Fixing

## Objective
Your task is to fix critical bugs and modernize the `pydream` codebase to be fully compatible with Python 3.11+ and NumPy 2.4+.

## Strict Constraints
1. **Retain Functionality**: The underlying mathematical and algorithmic logic of Differential Evolution Markov Chain (DREAM) sampling must remain strictly unchanged.
2. **Minimal Code Changes**: Only make modifications that are absolutely necessary to achieve compatibility and fix the identified bugs. Avoid stylistic refactoring or rewriting entire blocks of code unless required for version compatibility.
3. **Code Clarity & Efficiency**: Where changes are required, use standard, efficient, and readable Python/NumPy paradigms.
4. **NumPy 2.4+ Compatibility**: Ensure no deprecated NumPy types or functions are used (e.g., `np.float`, `np.int`, `np.bool` must be converted to native `float`, `int`, `bool`).

## Identified Bugs to Fix
You must resolve the two critical bugs identified in the `PYDREAM_BUGS_DOCUMENTATION.md`:

### Bug 1: The `multitry=2` Crash (NumPy Dimensionality Squeeze)
* **Issue**: When `multitry=2`, PyDream generates exactly 1 alternative point, which NumPy squeezes from a 2D shape `(1, N_parameters)` into a 1D shape `(N_parameters,)`. When passed to `pool.map()`, it iterates over the elements of the 1D array instead of passing the parameter array itself to the likelihood function.
* **Target Area**: `mt_evaluate_logps` and proposal point generation inside `pydream/Dream.py`.
* **Action**: Explicitly enforce a 2D shape for the `reference_pts` / `proposed_pts` array before passing it to `pool.map`. 
  *(Example: `if proposed_pts.ndim == 1: proposed_pts = proposed_pts.reshape(1, -1)`)*

### Bug 2: Nested Multiprocessing Bottleneck (`multitry` + `parallel=True`)
* **Issue**: When running with `parallel=True` and `multitry > 1`, the main loop spawns workers for each chain. However, inside each worker, `self.parallel=True` triggers `mt_evaluate_logps` to spawn a *sub-pool* of workers. This nested multiprocessing causes severe IPC overhead, serializing large objects unnecessarily, and thrashing the CPU.
* **Target Area**: `run_dream` in `pydream/core.py` and `mt_evaluate_logps` in `pydream/Dream.py`.
* **Action**: Separate chain-level parallelization from multitry-level parallelization. Ensure `mt_evaluate_logps` does not spawn a new `multiprocessing.Pool` if it is already executing inside a worker process. Use sequential list comprehensions/maps for multitry evaluations if chain-level multiprocessing is active.

## Modernization Checklist
1. **Python 3.11+ Standards**:
   - Verify the `multiprocessing` context management is handled correctly. `mp.get_context()` is currently used, ensure its implementation does not conflict with Python 3.11+ daemon process constraints.
   - Remove compatibility fallbacks for Python 2.x (e.g., checking `sys.version_info[0] < 3` for `assertRaisesRegexp`).
2. **NumPy 2.4+ Strict Compatibility**:
   - NumPy 2.x removed several aliases. Scan the codebase for `np.float`, `np.int`, `np.bool`, and `np.object` and replace them with standard Python types or valid NumPy `dtypes` (e.g., `np.float64`, `bool`).
   - Verify boolean masking and indexing arrays properly return 1D or ND arrays as expected.
   - Pay attention to `np.frombuffer` usages with multiprocessing shared arrays to ensure no strict casting violations exist.
   - `np.nan_to_num` and `np.linalg.norm` operations should be checked to ensure keyword arguments and behaviors align with NumPy 2.4+.

## Workflow Instructions for the Agent
When asked to implement these fixes:
1. Focus on one specific module or bug at a time.
2. Prioritize providing full diffs (Unified Diff Format) for modified files.
3. Verify the changes against the Constraints listed above before outputting the code.