# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:40:32 2016

@author: Erin
"""

from typing import Callable, Iterable, List, Tuple, Any
import numpy as np

class Model:
    
    def __init__(self, likelihood: Callable, sampled_parameters: Any):
        self.likelihood = likelihood
        if isinstance(sampled_parameters, list):
            self.sampled_parameters = sampled_parameters
        else:
            self.sampled_parameters = [sampled_parameters]
        
    def total_logp(self, q0: np.ndarray) -> Tuple[float, float]:

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