# Gemini Code Assist Agent Directives: PyDream Modernization & Bug Fixing

## Objective
Your task is to fix critical bugs and modernize the `pydream` codebase to be fully compatible with Python 3.11+ and NumPy 2.4+.

## Strict Constraints
1. **Retain Functionality**: The underlying mathematical and algorithmic logic of Differential Evolution Markov Chain (DREAM) sampling must remain strictly unchanged.
2. **Measured Refactoring**: While modernizing the codebase, allow for stylistic refactoring to meet basic Pylance, PEP-8, and type-hinting standards. Ensure these changes improve readability and maintainability without altering the mathematical logic.
3. **Code Clarity & Efficiency**: Where changes are required, use standard, efficient, and readable Python/NumPy paradigms.
4. **NumPy 2.4+ Compatibility**: Ensure no deprecated NumPy types or functions are used (e.g., `np.float`, `np.int`, `np.bool` must be converted to native `float`, `int`, `bool`).

## Identified Bugs
For a comprehensive list of previously identified bugs, their root causes, and resolution details, please refer to the `PYDREAM_BUGS_DOCUMENTATION.md` file. 

**Current Status:** As noted in the documentation, all previously identified critical bugs (such as the `multitry=2` crash and the nested multiprocessing bottleneck) are currently marked as **FIXED**. Maintain these fixes and refer to the documentation if investigating related regressions.

## Modernization Checklist
1. **Python 3.11+ Standards**:
   - Verify the `multiprocessing` context management is handled correctly. `mp.get_context()` is currently used, ensure its implementation does not conflict with Python 3.11+ daemon process constraints.
   - Remove compatibility fallbacks for Python 2.x (e.g., checking `sys.version_info[0] < 3` for `assertRaisesRegexp`).
2. **NumPy 2.4+ Strict Compatibility**:
   - NumPy 2.x removed several aliases. Scan the codebase for `np.float`, `np.int`, `np.bool`, and `np.object` and replace them with standard Python types or valid NumPy `dtypes` (e.g., `np.float64`, `bool`).
   - Verify boolean masking and indexing arrays properly return 1D or ND arrays as expected.
   - Pay attention to `np.frombuffer` usages with multiprocessing shared arrays to ensure no strict casting violations exist.
   - `np.nan_to_num` and `np.linalg.norm` operations should be checked to ensure keyword arguments and behaviors align with NumPy 2.4+.
3. **Pylance & Type Hinting (New)**:
   - Introduce basic type hinting (e.g., `int`, `float`, `bool`, `list`, `Callable` and basic `numpy.typing`) for function and method signatures.
   - Resolve basic Pylance warnings (e.g., unused imports, undefined variables, unreachable code).
   - Modernize string formatting (e.g., replace `'string %s' % var` with modern f-strings where it improves readability).
   - Clean up excessive empty lines and enforce standard indentation.

## Workflow Instructions for the Agent
When asked to implement these fixes:
1. Focus on one specific module or bug at a time.
2. First verify the nature of the bugs within the codebase, and then proceed to resolve them.
3. Prioritize providing full diffs (Unified Diff Format) for modified files.
4. Verify the changes against the Constraints listed above before outputting the code.