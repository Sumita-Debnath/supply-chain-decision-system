# src/disruption.py

import numpy as np

def apply_disruption(base_noise, active=False):

    if active:
        return np.random.normal(0.80, 0.30, base_noise.shape)
    return np.random.normal(0.95, 0.10, base_noise.shape)