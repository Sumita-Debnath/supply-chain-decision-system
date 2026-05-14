# 🚚 Supply Chain Decision Intelligence System

## 📌 Business Problem

In retail and e-commerce, one of the biggest challenges is:

**How much inventory should we keep?**

- Too little → stockouts → lost sales  
- Too much → high holding cost → blocked capital  

The goal is to **find the right balance between cost and service level**.

---

## 🎯 Objective

Build a system that helps answer:

> "What is the optimal inventory level that minimizes cost while maintaining high service levels?"

---

## 🧠 Approach

We built a **simulation-based decision system** instead of relying on static formulas.

### Step 1: Simulate Demand
- Demand is generated for multiple stores
- Includes randomness to reflect real-world variability
- Occasional demand spikes are also modeled

---

### Step 2: Apply Inventory Policy
- A fixed **Base Stock Level** is tested
- Inventory is distributed across stores based on demand

---

### Step 3: Add Real-World Uncertainty

To make the model realistic, we included:

- **Operational noise** → fulfillment is not perfect  
- **Supply disruptions** → sudden capacity drops  
- **Execution inefficiencies** → losses in warehouse / delivery  

---

### Step 4: Fulfill Demand
- Supply is capped by both demand and available capacity
- Ensures no over-delivery

---

### Step 5: Measure Performance

For each scenario, we calculate:

- **Service Level (SLA)** → how much demand was fulfilled  
- **Total Cost**, including:
  - Holding cost  
  - Stockout penalty  
  - Transport cost  

---

### Step 6: Run Multiple Simulations

- Each policy is tested across **many simulated scenarios**
- Final results are averaged for stability

---

### Step 7: Find Optimal Policy

Different strategies are supported:

- Cost-focused  
- Service-focused  
- Balanced (default)  

The system selects the **best inventory level based on the chosen strategy**.

---

## ⚙️ Key Assumptions

- Demand varies across stores and time  
- Supply is not perfectly reliable  
- Some inventory is always lost due to execution issues  
- Costs are proportional to inventory and unmet demand  

---

## 🛠 Techniques Used

- Monte Carlo Simulation  
- Scenario Analysis  
- Heuristic Optimization (scoring-based)  
- Proportional Allocation Logic  

---

## 📊 Results

The system provides:

- ✅ Optimal Base Stock Level  
- ✅ Expected Cost  
- ✅ Expected Service Level  
- ✅ Recommended inventory range  

---

## 📈 Business Impact

This system helps:

- Reduce unnecessary inventory costs  
- Improve product availability  
- Handle uncertainty in demand and supply  
- Make data-driven inventory decisions  

---

## 💡 Recommendations

- Operate within the **recommended inventory range**, not a single value  
- Increase inventory when:
  - Demand volatility is high  
  - Disruptions are frequent  

- Reduce inventory when:
  - Holding cost is high  
  - Demand is stable  

- Regularly update parameters based on real data  

---

## 🖥️ Dashboard

An interactive dashboard allows users to:

- Adjust business scenarios  
- Test different inventory levels  
- Visualize cost vs service trade-offs  
- Identify optimal decisions instantly  

---

## 🚀 How to Run

```bash
pip install -r requirements.txt


```python

```
