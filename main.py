import yaml
import numpy as np
import pandas as pd
from src.simulator import run_simulation


def main():

    # -------- LOAD CONFIG --------
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # -------- POLICY RANGE --------
    policies = np.arange(
        config["policy"]["min"],
        config["policy"]["max"] + 1,
        config["policy"]["step"]
    )

    results = []

    # -------- RUN SIMULATION --------
    for p in policies:
        cost, sla = run_simulation(p, config)

        results.append({
            "Policy": p,
            "Cost": cost,
            "SLA": sla
        })

    df = pd.DataFrame(results)

    # -------- FIND OPTIMAL --------
    df["Score"] = df["SLA"] - 0.0001 * df["Cost"]
    optimal = df.loc[df["Score"].idxmax()]
    baseline = df.iloc[0]

    # -------- PRINT RESULTS --------
    print("\n=== OPTIMAL POLICY ===")
    print(optimal)

    print("\n=== BASELINE POLICY ===")
    print(baseline)

    print("\nSYSTEM RUN COMPLETE ✔")


if __name__ == "__main__":
    main()