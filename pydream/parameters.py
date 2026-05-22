# -*- coding: utf-8 -*-

from typing import Any, List, Tuple

import numpy as np


class SampledParam:
    """A SciPy-based parameter prior class.

    Parameters
    ----------
    scipy_distribution: SciPy continuous random variable class
        A SciPy statistical distribution (i.e. scipy.stats.norm)
    args:
        Arguments for the SciPy distribution
    kwargs:
        keyword arguments for the SciPy distribution

        """
    def __init__(self, scipy_distribution: Any, *args: Any, **kwargs: Any) -> None:
        self.dist = scipy_distribution(*args, **kwargs)
        self.dsize = self.random().size

    def interval(self, alpha: float = 1) -> Tuple[Any, Any]:
        """Return the interval for a given alpha value."""

        return self.dist.interval(alpha)

    def random(self, reseed: bool = False) -> np.ndarray:
        """Return a random value drawn from this prior."""
        if reseed:
            random_seed = np.random.RandomState()
        else:
            random_seed = None

        return self.dist.rvs(random_state=random_seed)

    def prior(self, q0: np.ndarray) -> float:
        """Return the prior log probability given a point.

        Parameters
        ----------
        q0: array
            A location in parameter space.
        """
        logp = np.sum(self.dist.logpdf(q0))

        return logp

class FlatParam(SampledParam):
    """A Flat parameter class (returns 0 at all locations).

    Parameters
    ----------
    test_value: array
        Representative value for the parameter.  Used to infer the parameter dimension, which is needed in the DREAM algorithm.

    """

    def __init__(self, test_value: np.ndarray) -> None:
        self.dsize = test_value.size

    def prior(self, q0: np.ndarray) -> float:
        return 0

    def interval(self, alpha: float = 1) -> List[List[float]]:
        """Return the interval for a given alpha value."""

        lower = [-np.inf] * self.dsize
        upper = [np.inf] * self.dsize
        return [lower, upper]
