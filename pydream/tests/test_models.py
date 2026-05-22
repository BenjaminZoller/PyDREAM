# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:58:09 2016

@author: Erin

#Parameters defined for simple example statistical models for testing DREAM
"""

from typing import Callable, List, Tuple

import numpy as np
from scipy.stats import norm, uniform

from pydream.parameters import SampledParam


def onedmodel() -> Tuple[List[SampledParam], Callable[[np.ndarray], float]]:
    """Create a one-dimensional model with a normal prior.

    Returns
    -------
    Tuple[List[SampledParam], Callable[[np.ndarray], float]]
        A tuple containing the parameter list and the likelihood function.
    """

    mu = -2
    sd = 3
    x = SampledParam(norm, loc=mu, scale=sd)
    like = simple_likelihood

    return [x], like

def multidmodel() -> Tuple[List[SampledParam], Callable[[np.ndarray], float]]:
    """Create a multi-dimensional model with a normal prior.

    Returns
    -------
    Tuple[List[SampledParam], Callable[[np.ndarray], float]]
        A tuple containing the parameter list and the likelihood function.
    """

    mu = np.array([-6.6, 3, 1.0, -.12])
    sd = np.array([.13, 5, .9, 1.0])

    x = SampledParam(norm, loc=mu, scale=sd)
    like = simple_likelihood

    return [x], like

def multidmodel_uniform() -> Tuple[List[SampledParam], Callable[[np.ndarray], float]]:
    """Create a multi-dimensional model with uniform priors.

    Returns
    -------
    Tuple[List[SampledParam], Callable[[np.ndarray], float]]
        A tuple containing the parameter list and the likelihood function.
    """

    lower = np.array([-5, -9, 5, 3])
    upper = np.array([10, 2, 7, 8])
    range = upper-lower

    x = SampledParam(uniform, loc=lower, scale=range)
    like =simple_likelihood

    return [x], like

def simple_likelihood(param: np.ndarray) -> float:
    """Evaluate a simple flat likelihood.

    Parameters
    ----------
    param : numpy.ndarray
        The parameter vector.

    Returns
    -------
    float
        The computed log-likelihood.
    """

    return np.sum(param + 3)
