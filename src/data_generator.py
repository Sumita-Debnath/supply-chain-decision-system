import numpy as np

def generate_demand(n_nodes=5):
    demand = np.random.normal(loc=100, scale=20, size=n_nodes)
    return np.maximum(demand, 0)