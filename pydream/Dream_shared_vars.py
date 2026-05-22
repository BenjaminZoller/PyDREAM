# -*- coding: utf-8 -*-
from typing import Any

# Multiprocessing shared variables (populated dynamically at runtime by core._mp_dream_init)
history: Any = None
current_positions: Any = None
nchains: Any = None
cross_probs: Any = None
ncr_updates: Any = None
delta_m: Any = None
gamma_level_probs: Any = None
ngamma_updates: Any = None
delta_m_gamma: Any = None
count: Any = None
history_seeded: Any = None
burnin_barrier: Any = None
