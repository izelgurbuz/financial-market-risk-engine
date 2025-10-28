import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from core.risk_engine import bond_dv01, fx_delta


def monte_carlo_var(
    n_sims=10_000,
    position_gbp=10_000,
    base_fx_rate=1.25,
    face_value=1_000,
    base_yield=0.05,
    fx_vol=0.01,  # 1% daily volatility
    rate_vol=0.0025,  # 0.25% daily volatility
    confidence=0.95,
):
    """
    Monte Carlo simulation for a portfolio that is LONG USD (short GBP)
    and holds a fixed-rate bond.  Computes VaR and P&L distribution.
    """

    # Sensitivities
    fx_moves, fx_pnl_curve = fx_delta(position_gbp, base_fx_rate)
    fx_d = -(fx_pnl_curve[11] - fx_pnl_curve[10])  # long USD / short GBP
    dv01 = bond_dv01(face_value, 0.04, 5, base_yield)

    #  Random market moves
    fx_shocks = np.random.normal(0, fx_vol, n_sims)  # ΔFX %
    rate_shocks = np.random.normal(0, rate_vol, n_sims)  # Δyields %

    # Linear P&L approximation
    fx_pnl = fx_d * (fx_shocks * 100)
    bond_pnl = -dv01 * (rate_shocks * 10000)
    total_pnl = fx_pnl + bond_pnl

    # VaR calculation
    var_threshold = np.percentile(total_pnl, (1 - confidence) * 100)
    var_value = -var_threshold
    expected_loss = total_pnl.mean()
    worst_loss = total_pnl.min()

    summary = pd.Series(
        {
            "Confidence": confidence,
            "VaR (£)": round(var_value, 2),
            "Expected Loss (£)": round(expected_loss, 2),
            "Worst Loss (£)": round(worst_loss, 2),
            "FX Delta (£/1 %)": round(fx_d, 2),
            "Bond DV01 (£/1 bp)": round(dv01, 4),
        }
    )

    # Plot distribution
    plt.figure(figsize=(9, 5))
    plt.hist(total_pnl, bins=60, color="#2E86AB", alpha=0.7)
    plt.axvline(
        var_threshold,
        color="red",
        linestyle="--",
        label=f"{int(confidence * 100)} % VaR",
    )
    plt.title("Monte Carlo Portfolio P&L Distribution")
    plt.xlabel("Simulated P&L (£)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

    return summary, total_pnl
