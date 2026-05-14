import streamlit as st
import pandas as pd
import numpy as np
import yaml
import sys
import os
import matplotlib.pyplot as plt

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.simulator import run_simulation

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Supply Chain Decision System", layout="wide")

st.title("🚚 Supply Chain Decision Intelligence System")
st.markdown("### AI-Powered Inventory Optimization & Scenario Simulator")

# ---------------- LOAD CONFIG ----------------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# ---------------- SIDEBAR ----------------

# ✅ MOVE MODE TO TOP
st.sidebar.header("🎯 Optimization Strategy")
mode = st.sidebar.radio(
    "Optimization Mode",
    ["Cost Focus", "Balanced", "Service Focus"]
)

st.sidebar.markdown("---")

st.sidebar.header("⚙ Scenario Simulator")

policy_input = st.sidebar.slider(
    "Base Stock Level (Inventory Target)",
    50, 500, 200, step=50
)

demand_scale = st.sidebar.slider("Demand Volatility", 0.8, 1.5, 1.0)

disruption_prob = st.sidebar.slider(
    "Disruption Probability", 0.0, 0.5,
    config["disruption"]["probability"]
)

holding_rate = st.sidebar.slider(
    "Holding Cost (%)", 0.1, 0.4,
    config["cost"]["holding_rate_annual"]
)

stockout_penalty = st.sidebar.slider(
    "Stockout Penalty", 0.2, 0.8,
    config["cost"]["stockout_penalty"]
)

transport_rate = st.sidebar.slider(
    "Transport Cost (%)", 0.02, 0.1,
    config["cost"]["transport_rate"]
)

# Apply config
config["disruption"]["probability"] = disruption_prob
config["cost"]["holding_rate_annual"] = holding_rate
config["cost"]["stockout_penalty"] = stockout_penalty
config["cost"]["transport_rate"] = transport_rate

# ---------------- SINGLE SCENARIO ----------------
st.markdown("## 🔍 Scenario Result")

cost, sla = run_simulation(policy_input, config)

col1, col2 = st.columns(2)
col1.metric("📦 SLA", f"{sla:.2%}")
col2.metric("💰 Cost", f"₹{cost:.0f}")

# ---------------- FULL OPTIMIZATION ----------------
st.markdown("## 📊 Optimization View")

@st.cache_data
def run_full_simulation(config, mode):

    policies = np.arange(
        config["policy"]["min"],
        config["policy"]["max"] + 1,
        config["policy"]["step"]
    )

    results = []

    # first pass for normalization
    cost_list = []
    for p in policies:
        c, s = run_simulation(p, config)
        cost_list.append(c)

    max_cost = max(cost_list) + 1e-6

    # second pass
    for i, p in enumerate(policies):
        cost = cost_list[i]
        _, sla = run_simulation(p, config)

        if mode == "Cost Focus":
            score = -cost
        elif mode == "Service Focus":
            score = sla
        else:
            score = sla - (cost / max_cost)

        results.append({
            "Base Stock Level": p,
            "Cost": cost,
            "SLA": sla,
            "Score": score
        })

    df = pd.DataFrame(results)

    # normalize cost for plotting
    df["Cost_norm"] = (
        (df["Cost"] - df["Cost"].min()) /
        (df["Cost"].max() - df["Cost"].min() + 1e-6)
    )

    return df

df = run_full_simulation(config, mode)
# Ensure outputs folder exists
os.makedirs("outputs", exist_ok=True)

# Save results
df.to_csv("outputs/simulation_results.csv", index=False)

optimal = df.loc[df["Score"].idxmax()]
baseline = df.iloc[0]

# ---------------- KPI ----------------
st.markdown("## 📊 Key Metrics")

cost_reduction = (baseline["Cost"] - optimal["Cost"]) / baseline["Cost"] * 100
sla_improvement = (optimal["SLA"] - baseline["SLA"]) * 100

col1, col2, col3 = st.columns(3)
col1.metric("💰 Cost Reduction", f"{cost_reduction:.2f}%")
col2.metric("📈 SLA Improvement", f"{sla_improvement:.2f}%")
col3.metric("🎯 Optimal Base Stock", int(optimal["Base Stock Level"]))

# ---------------- CHARTS ----------------
st.markdown("## 📊 Trade-off Analysis")

col1, col2 = st.columns(2)

# LEFT: Cost curve
with col1:
    st.subheader("📈 Cost vs Base Stock Level")

    fig1, ax1 = plt.subplots()
    ax1.plot(df["Base Stock Level"], df["Cost"], marker='o')
    ax1.set_xlabel("Base Stock Level")
    ax1.set_ylabel("Cost")
    os.makedirs("docs", exist_ok=True)

    fig1.savefig("docs/cost_curve.png")
    st.pyplot(fig1)


# RIGHT: Pareto
with col2:
    st.subheader("🎯 Cost vs SLA (Pareto Frontier)")

    fig2, ax2 = plt.subplots()

    # add slight jitter to avoid overlap
    jitter = np.random.normal(0, 0.002, size=len(df))

    scatter = ax2.scatter(
        df["Cost_norm"],
        df["SLA"] + jitter,
        c=df["Base Stock Level"],
        cmap="viridis"
    )

    # optimal point
    ax2.scatter(
        optimal["Cost_norm"],
        optimal["SLA"],
        marker="*",
        s=250
    )

    ax2.set_xlabel("Normalized Cost")
    ax2.set_ylabel("SLA")

    plt.colorbar(scatter, ax=ax2, label="Base Stock Level")

    fig2.savefig("docs/pareto.png")
    st.pyplot(fig2)

# ---------------- RECOMMENDATION ----------------
st.markdown("## 📌 Recommendation")

lower = optimal["Base Stock Level"] - config["policy"]["step"]
upper = optimal["Base Stock Level"] + config["policy"]["step"]

st.success(f"""
👉 Optimal Base Stock Level: {int(optimal['Base Stock Level'])}  
👉 Recommended Range: {int(lower)} – {int(upper)}

Balance cost vs service level  
Avoid extreme inventory positions  
Monitor demand volatility and disruptions  
""")

# ---------------- TABLE ----------------
st.markdown("## 📄 Detailed Results")
st.dataframe(df)
st.download_button(
    label="📥 Download Results as CSV",
    data=df.to_csv(index=False),
    file_name="simulation_results.csv",
    mime="text/csv"
)