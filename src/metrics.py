import numpy as np

def compute_metrics(demand, supply, holding_rate, stockout_penalty, transport_rate):

    fulfilled = np.sum(supply)
    total_demand = np.sum(demand) + 1e-6

    sla = fulfilled / total_demand

    # ₹ assumptions
    unit_price = 100

    inventory_value = np.sum(supply) * unit_price
    unmet_value = np.sum(demand - supply) * unit_price

    # convert annual holding → monthly approx
    holding_cost = inventory_value * (holding_rate / 12)

    stockout_cost = unmet_value * stockout_penalty

    transport_cost = inventory_value * transport_rate

    total_cost = holding_cost + stockout_cost + transport_cost

    return float(total_cost), float(sla)