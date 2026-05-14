import numpy as np
from src.data_generator import generate_demand
from src.metrics import compute_metrics


def run_simulation(policy, config, iterations=200):

    costs = []
    slas = []

    for _ in range(iterations):

        # -------- DEMAND --------
        demand = generate_demand()
        demand = np.maximum(demand, 0)

        # -------- DEMAND SHOCK --------
        if np.random.rand() < 0.2:
            demand *= np.random.uniform(1.1, 1.3)

        # -------- INVENTORY --------
        total_inventory = policy * len(demand)

        demand_sum = np.sum(demand) + 1e-6
        allocation = (demand / demand_sum) * total_inventory

        # -------- NOISE --------
        noise = np.random.normal(
            config["noise"]["mean"],
            config["noise"]["std"],
            len(demand)
        )
        noise = np.clip(noise, 0.7, 1.1)

        capacity = allocation * noise

        # -------- DISRUPTION --------
        if np.random.rand() < config["disruption"]["probability"]:
            capacity *= np.random.uniform(0.8, 0.95, len(demand))

        # -------- FULFILLMENT --------
        supply = np.minimum(demand, capacity)

        # -------- REALISTIC LOSS --------
        inefficiency = np.random.uniform(0.88, 0.95, len(demand))
        supply = supply * inefficiency

        # -------- STABILITY GUARD --------
        supply = np.minimum(supply, demand)
        supply = np.maximum(supply, 0)

        # -------- METRICS --------
        cost, sla = compute_metrics(
            demand,
            supply,
            config["cost"]["holding_rate_annual"],
            config["cost"]["stockout_penalty"],
            config["cost"]["transport_rate"]
        )

        costs.append(cost)
        slas.append(sla)

    return float(np.mean(costs)), float(np.mean(slas))