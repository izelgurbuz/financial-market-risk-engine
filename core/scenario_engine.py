import matplotlib.pyplot as plt
import pandas as pd

from core.risk_engine import bond_dv01, fx_delta


def simulate_scenarios(
    position_gbp=10_000, base_fx_rate=1.25, face_value=1_000, base_yield=0.05
):
    """
    Scenario & stress testing for a portfolio LONG USD (short GBP)
    holding a fixed-rate bond.

    """

    scenarios = {
        "Mild_Positive": (0.01, -0.002),  # GBP weakens 1%, yields -0.2%
        "Mild_Negative": (-0.01, 0.002),  # GBP strengthens 1%, yields +0.2%
        "Moderate_Pos": (0.05, -0.005),  # GBP weakens 5%, yields -0.5%
        "Moderate_Neg": (-0.05, 0.005),  # GBP strengthens 5%, yields +0.5%
        "Severe_Pos": (0.10, -0.02),  # GBP weakens 10%, yields -2%
        "Severe_Neg": (-0.10, 0.02),  # GBP strengthens 10%, yields +2%
    }

    fx_moves, fx_pnl_curve = fx_delta(position_gbp, base_fx_rate)
    fx_d = fx_pnl_curve[11] - fx_pnl_curve[10]  # ✅ FIXED: correct directional delta
    dv01 = bond_dv01(face_value, 0.04, 5, base_yield)

    results = []

    for name, (fx_move, rate_move) in scenarios.items():
        fx_pnl = fx_d * (fx_move * 100)
        bond_pnl = -dv01 * (rate_move * 10000)
        total = fx_pnl + bond_pnl

        results.append(
            {
                "Scenario": name,
                "GBP_Move(%)": fx_move * 100,
                "Rate_Move(%)": rate_move * 100,
                "FX_PnL(£)": round(fx_pnl, 2),
                "Bond_PnL(£)": round(bond_pnl, 2),
                "Total_PnL(£)": round(total, 2),
            }
        )

    return pd.DataFrame(results)


def plot_scenario_results(df):
    """
    Bar chart showing total P&L for each scenario.

    """
    colors = ["#2E86AB" if x > 0 else "#C70039" for x in df["Total_PnL(£)"]]
    plt.figure(figsize=(10, 5))
    plt.bar(df["Scenario"], df["Total_PnL(£)"], color=colors)
    plt.title("Portfolio P&L under FX/Rate Scenarios")
    plt.ylabel("Total P&L (£)")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
