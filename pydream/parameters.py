# -*- coding: utf-8 -*-

from typing import Any, List, Tuple

import numpy as np


class SampledParam:
    """A SciPy-based parameter prior class.

    Parameters
    ----------
    scipy_distribution : Any
        A SciPy statistical distribution class (e.g., scipy.stats.norm).
    *args : Any
        Positional arguments to initialize the SciPy distribution.
    **kwargs : Any
        Keyword arguments to initialize the SciPy distribution.
    """
    def __init__(self, scipy_distribution: Any, *args: Any, **kwargs: Any) -> None:
        self.dist = scipy_distribution(*args, **kwargs)
        self.dsize = self.random().size

    def interval(self, alpha: float = 1) -> Tuple[Any, Any]:
        """Return the interval for a given alpha value.

        Parameters
        ----------
        alpha : float, optional
            The probability that the random variable falls within the returned interval.
            Default is 1.

        Returns
        -------
        Tuple[Any, Any]
            A tuple containing the lower and upper bounds of the interval.
        """

        return self.dist.interval(alpha)

    def random(self, reseed: bool = False) -> np.ndarray:
        """Return a random value drawn from this prior.

        Parameters
        ----------
        reseed : bool, optional
            If True, creates a new NumPy RandomState to draw the value,
            ensuring independence from the global RNG state. Default is False.

        Returns
        -------
        numpy.ndarray
            A random draw from the underlying SciPy distribution.
        """
        if reseed:
            random_seed = np.random.RandomState()
        else:
            random_seed = None

        return self.dist.rvs(random_state=random_seed)

    def prior(self, q0: np.ndarray) -> float:
        """Return the prior log probability given a point.

        Parameters
        ----------
        q0 : numpy.ndarray
            A location in parameter space.

        Returns
        -------
        float
            The log probability density evaluated at `q0`.
        """
        logp = np.sum(self.dist.logpdf(q0))

        return logp

class FlatParam(SampledParam):
    """A Flat parameter prior class (returns a log probability of 0.0 at all locations).

    Parameters
    ----------
    test_value : numpy.ndarray
        Representative value for the parameter. Used to infer the parameter
        dimension, which is needed by the DREAM algorithm.
    """

    def __init__(self, test_value: np.ndarray) -> None:
        self.dsize = test_value.size

    def prior(self, q0: np.ndarray) -> float:
        """Return the prior log probability given a point.

        For a FlatParam, this always returns 0.0, representing an improper uniform prior
        over the entire parameter space.

        Parameters
        ----------
        q0 : numpy.ndarray
            A location in parameter space.

        Returns
        -------
        float
            Always returns 0.0.
        """
        return 0.0

    def interval(self, alpha: float = 1) -> List[List[float]]:
        """Return the infinite interval for the flat prior.

        Parameters
        ----------
        alpha : float, optional
            Included for API compatibility with SampledParam. Default is 1.

        Returns
        -------
        List[List[float]]
            A list containing the lower and upper bounds ([-inf, inf] for each dimension).
        """

        lower = [-np.inf] * self.dsize
        upper = [np.inf] * self.dsize
        return [lower, upper]
