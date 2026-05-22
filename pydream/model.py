# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:40:32 2016

@author: Erin
"""

from typing import Any, Callable, List, Tuple, Union

import numpy as np


class Model:
    """A wrapper class for the user-defined likelihood and prior models.

    Parameters
    ----------
    likelihood : Callable[[numpy.ndarray], float]
        A user-defined function that takes a parameter vector and returns the log-likelihood.
    sampled_parameters : Union[Any, List[Any]]
        A list of SampledParam instances defining the prior distributions.
    """

    def __init__(self, likelihood: Callable[[np.ndarray], float], sampled_parameters: Union[Any, List[Any]]) -> None:
        self.likelihood = likelihood
        if isinstance(sampled_parameters, list):
            self.sampled_parameters = sampled_parameters
        else:
            self.sampled_parameters = [sampled_parameters]

    def total_logp(self, q0: np.ndarray) -> Tuple[float, float]:
        """Calculate the total log probability (prior + likelihood) for a given point.

        Parameters
        ----------
        q0 : numpy.ndarray
            A location in parameter space.

        Returns
        -------
        Tuple[float, float]
            A tuple containing the log prior probability and the log likelihood.
        """

        prior_logp = 0
        var_start = 0
        for param in self.sampled_parameters:
            var_end = param.dsize + var_start
            try:
                prior_logp += param.prior(q0[var_start:var_end])
            except IndexError:
                #raised if q0 is a single scalar
                prior_logp += param.prior(q0)
            var_start += param.dsize

        loglike = self.likelihood(q0)

        return prior_logp, loglike
