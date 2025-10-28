import matplotlib.pyplot as plt
import numpy as np

from core.bond_pricer import price_bond


def fx_delta(position_gbp: float = 10_000, base_fx_rate: float = 1.25):
    """
    Compute how the GBP value of a USD position changes as FX rate moves.
    This represents true directional P&L vs. the base FX rate.


    """
    usd_amount = position_gbp * base_fx_rate

    fx_moves = np.linspace(-0.05, 0.05, 21)
    pnl_gbp = []

    for move in fx_moves:
        shocked_rate = base_fx_rate * (1 + move)
        value_in_gbp = usd_amount / shocked_rate
        pnl_vs_base = value_in_gbp - position_gbp
        pnl_gbp.append(pnl_vs_base)

    return fx_moves * 100, pnl_gbp


def bond_dv01(face_value=1000, coupon_rate=0.04, maturity=5, base_yield=0.05):
    """
    DV01: measures bond price change (£) for a 1 basis point (0.01%) change in yield.

    """
    base_price = price_bond(face_value, coupon_rate, maturity, base_yield)
    up_price = price_bond(face_value, coupon_rate, maturity, base_yield + 0.0001)
    dv01 = base_price - up_price
    return dv01


def portfolio_risk_summary(position_gbp=10_000, base_fx_rate=1.25, face_value=1000):
    _, fx_pnl = fx_delta(position_gbp, base_fx_rate)

    bond_risk = bond_dv01(face_value)
    return {
        "FX Δ (GBP P&L per +1%)": fx_pnl[11] - fx_pnl[10] if len(fx_pnl) > 11 else None,
        "Bond DV01 (£ change per 1bp)": bond_risk,
    }


def plot_portfolio_sensitivity():
    """
    Plot directional portfolio sensitivity curves for FX and bonds.
    FX curve shows P&L vs FX move; bond curve shows DV01 vs yield move.
    """
    # FX curve
    fx_x, fx_y = fx_delta(position_gbp=10_000, base_fx_rate=1.25)

    # Bond DV01 curve
    rate_moves = np.linspace(-0.01, 0.01, 21)
    bond_y = [bond_dv01(base_yield=0.05 + r) for r in rate_moves]

    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    ax1.plot(
        fx_x,
        fx_y,
        color="blue",
        linewidth=2,
        label="FX P&L vs Base (£)",
    )
    ax1.set_xlabel("FX Move (%) or Yield Move (bps)")
    ax1.set_ylabel("FX P&L (£)", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2.plot(
        rate_moves * 10000,
        bond_y,
        color="orange",
        linewidth=2,
        label="Bond DV01 (£ per 1bp)",
    )
    ax2.set_ylabel("Bond DV01 (£ per 1bp)", color="orange")
    ax2.tick_params(axis="y", labelcolor="orange")

    plt.title("Portfolio Sensitivity Curves (Directional P&L vs Base)")
    fig.tight_layout()
    plt.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.show()
