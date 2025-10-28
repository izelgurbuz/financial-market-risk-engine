import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def price_bond(
    face_value: float = 1000,
    coupon_rate: float = 0.04,
    maturity_years: int = 5,
    market_rate: float = 0.05,
    freq: int = 1,
):
    """
    Compute the present value of a fixed-coupon bond.
    """

    coupon = face_value * coupon_rate / freq
    periods = maturity_years * freq
    discount_factors = [
        1 / (1 + market_rate / freq) ** t for t in range(1, periods + 1)
    ]
    price = (
        sum(coupon * d_factor for d_factor in discount_factors)
        + face_value * discount_factors[-1]
    )

    return price


def bond_duration(
    face_value: float = 1000,
    coupon_rate: float = 0.04,
    maturity_years: int = 5,
    market_rate: float = 0.05,
    freq: int = 1,
):
    coupon = face_value * coupon_rate / freq
    periods = maturity_years * freq
    pv_factors = np.array(
        [((1 / 1 + market_rate / freq) ** t) for t in range(1, periods + 1)]
    )
    cashflows = np.array([coupon] * periods)
    cashflows[-1] += face_value
    weights = pv_factors * cashflows
    duration = np.sum(weights * np.arange(1, periods + 1)) / np.sum(weights)
    return duration / freq  # convert it to year


def simulate_rate_sensitivity():
    face = 1000
    coupon = 0.04
    maturity = 5

    rates = np.linspace(0.01, 0.05, 50)
    prices = [price_bond(face, coupon, maturity, r) for r in rates]

    df = pd.DataFrame({"Rate": rates, "Price": prices})
    plt.figure(figsize=(8, 4))
    plt.plot(df["Rate"] * 100, df["Price"])
    plt.title("Bond Price vs Market Rate")
    plt.xlabel("Market Rate (%)")
    plt.ylabel("Bond Price (£)")
    plt.grid(True)
    plt.show()

    return df
