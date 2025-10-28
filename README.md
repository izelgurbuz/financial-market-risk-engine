#  Financial Market Risk Engine

_A modular quantitative-finance learning project_

---

## Overview

This project implements a **mini market-risk engine** to measure exposure to **foreign-exchange (FX)** and **interest-rate** movements.  
It builds up from first principles: simulating market prices, valuing bonds, computing sensitivities, and quantifying risk through **stress testing** and **Value-at-Risk (VaR)**.

All code is written from scratch in Python for full transparency

---
<img width="947" height="391" alt="Screenshot 2025-10-28 at 18 42 45" src="https://github.com/user-attachments/assets/fcd4fbfd-15c4-4e07-be3a-a62d34dd57fe" />
<img width="983" height="497" alt="Screenshot 2025-10-28 at 18 43 06" src="https://github.com/user-attachments/assets/cb39d665-953b-4bf3-bf43-e587ef3faa83" />
<img width="886" height="488" alt="Screenshot 2025-10-28 at 18 26 37" src="https://github.com/user-attachments/assets/431023da-a5b7-43d7-acb9-99ae1b7ec008" />

## Components Implemented

| Module               | Purpose                                                                                 |
| -------------------- | --------------------------------------------------------------------------------------- |
| `fx_simulator.py`    | Simulates GBP/USD exchange-rate paths and computes daily/annualized volatility.         |
| `bond_pricer.py`     | Values fixed-coupon bonds across a range of yields using discounted cashflows.          |
| `risk_engine.py`     | Computes **FX Δ** (currency exposure) and **Bond DV01** (rate sensitivity).             |
| `scenario_engine.py` | Applies deterministic **what-if market shocks** for stress testing.                     |
| `var_engine.py`      | Runs **Monte Carlo simulations** of random FX and rate moves to estimate daily **VaR**. |

---

## Key Numerical Results

### FX Simulation

| Metric                     | Value       |
| -------------------------- | ----------- |
| Estimated daily volatility | **0.559 %** |
| Annualized volatility      | **8.87 %**  |

Example of simulated FX path:

| Day | Return    | FX Rate |
| --- | --------- | ------- |
| 1   | 0.002980  | 1.2537  |
| 2   | −0.000830 | 1.2527  |
| 3   | 0.003886  | 1.2576  |
| 4   | 0.009138  | 1.2690  |
| 5   | −0.001405 | 1.2673  |

---

### Bond Pricing & Duration

| Yield  | Price (£) |
| ------ | --------- |
| 1.00 % | 1145.60   |
| 1.08 % | 1141.30   |
| 1.16 % | 1137.02   |
| 1.24 % | 1132.76   |
| 1.33 % | 1128.51   |

**Modified Duration ≈ 4.71 years**  
**DV01 ≈ £0.4209**

---

### Portfolio Sensitivities

| Metric                                   | Value   |
| ---------------------------------------- | ------- |
| **FX Δ** (GBP P&L per +1 % move)         | −49.75  |
| **Bond DV01** (GBP per 1 bp rate change) | +0.4209 |

**Interpretation:**

> The portfolio loses about £50 if GBP strengthens 1 %,  
> and gains about £0.42 for each 1 bp drop in yields.

---

### Monte Carlo VaR Results

| Metric                  | Value      |
| ----------------------- | ---------- |
| Confidence              | 95 %       |
| **Value-at-Risk (VaR)** | **£83.82** |
| Expected Loss           | −£0.25     |
| Worst Loss              | −£201.22   |
| FX Δ (£/1 %)            | 49.75      |
| Bond DV01 (£/1 bp)      | 0.4209     |

→ There is approximately a **5 % probability that a one-day loss exceeds £84.**

---

## Example Visuals

### **Portfolio Sensitivity**

_(Blue = FX P&L, Orange = Bond DV01)_  
`assets/portfolio_sensitivity.png`

---

### **Scenario & Stress Tests**

| Scenario                         | GBP Move (%) | Rate Move (%) | FX P&L (£) | Bond P&L (£) | **Total P&L (£)** |
| -------------------------------- | ------------ | ------------- | ---------- | ------------ | ----------------- |
| Mild (GBP ↑ 1 %, rates ↓ 0.2 %)  | +1.0         | −0.2          | −49.8      | +0.84        | −49.0             |
| Mild (GBP ↓ 1 %, rates ↑ 0.2 %)  | −1.0         | +0.2          | +49.8      | −0.84        | +49.0             |
| Severe (GBP ↓ 10 %, rates ↑ 2 %) | −10.0        | +2.0          | +498.0     | −8.4         | +490.0            |

---

### **Monte Carlo VaR Distribution**

`assets/var_distribution.png`  
(Blue = simulated P&L; Red = 95 % VaR cut-off.)

---

## Theory Recap — Scenario vs Stress Testing

| Type                  | Description                                                     | Typical Shocks | Purpose                    |
| --------------------- | --------------------------------------------------------------- | -------------- | -------------------------- |
| **Scenario Analysis** | Apply plausible, moderate market changes (e.g. ±1–5 % FX).      | Small          | Routine exposure review    |
| **Stress Testing**    | Apply extreme, but credible shocks (e.g. ±10 % FX, ±2 % rates). | Large          | Resilience / capital tests |

Both rely on your pricing logic — the shock simply alters `base_fx_rate` or `base_yield` and recalculates portfolio P&L.

---

## What I’ve Learned

- How FX and bond market parameters translate into real currency P&L.
- The inverse link between yield and price, and how **DV01** quantifies it.
- How to express currency exposure via **FX Δ**.
- The difference between **deterministic stress tests** and **probabilistic VaR**.
- Building transparent, modular risk logic in Python from scratch.

---

## Next Phase

The next addition will extend this engine with **PyTorch-based predictive modelling** —  
training a neural network to forecast next-day FX returns or volatility and integrating those forecasts into a _forecast-aware VaR_ module.

---

## Tech Stack

Python 3.11 | NumPy | Pandas | Matplotlib  
_(PyTorch planned for upcoming ML extension.)_

---

## Run Locally

```bash
git clone https://github.com/<your-username>/financial-market-risk-engine.git
cd financial-market-risk-engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
