# src/network.py

import numpy as np

def propagate_supply(dc_supply, fc_count, noise_level):

    fc_supply = dc_supply / fc_count
    noise = np.random.normal(0.95, noise_level, fc_count)

    return fc_supply * noise