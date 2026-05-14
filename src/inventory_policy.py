import numpy as np

def apply_inventory_policy(demand, policy_level):
    """
    Distributes inventory across nodes based on demand proportion,
    with realistic constraints.
    """

    # total inventory available
    total_inventory = policy_level * len(demand)

    # avoid divide-by-zero
    total_demand = np.sum(demand) + 1e-6

    # proportional allocation
    allocation = (demand / total_demand) * total_inventory

    # cannot exceed demand
    supply = np.minimum(allocation, demand)

    # 🔥 REAL-WORLD FRICTION (KEY)
    inefficiency = np.random.uniform(0.88, 0.95, size=len(demand))
    supply = supply * inefficiency

    return supply