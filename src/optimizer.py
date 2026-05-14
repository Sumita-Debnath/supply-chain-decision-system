import numpy as np

def get_optimal(df):
    """
    Pareto-style optimal policy:
    balances SLA and Cost
    """
    best_idx = np.argmax(df["SLA"] - 0.001 * df["Cost"])
    return df.iloc[best_idx]


def get_baseline(df):
    """
    Baseline policy = closest to 100 (industry default reference)
    """
    baseline_policy = 100

    df = df.copy()
    df["diff"] = np.abs(df["Policy"] - baseline_policy)

    return df.loc[df["diff"].idxmin()].drop("diff")