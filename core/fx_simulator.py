import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def simulate_fx_path(
    start_rate: float = 1.25, days: int = 100, daily_vol: float = 0.005, seed: int = 42
):
    """
    Simulates an FX rate (e.g. GBP/USD) using random daily returns.

    Parameters:

    start_rate: Initial fx rate (e.g. 1.25 mean £1 = $1.25)
    days: Number of trading days to simulate
    daily_vol : Standard deviation of daily percentage changes
    seed: Random seed for reproducibility
    """

    np.random.seed(seed)
    daily_returns = np.random.normal(0, daily_vol, days)

    fx_rates = start_rate * np.cumprod(1 + daily_returns)

    df = pd.DataFrame(
        {"Day": np.arange(1, days + 1), "Return": daily_returns, "FX_Rate": fx_rates}
    )
    initial_investment_gbp = 10_000
    initial_rate = df["FX_Rate"].iloc[0]
    usd_amount = initial_investment_gbp * initial_rate

    final_rate = df["FX_Rate"].iloc[-1]
    final_gbp_value = usd_amount / final_rate
    profit = final_gbp_value - initial_investment_gbp

    print(f"Start FX Rate: {initial_rate:.3f}")
    print(f"End FX Rate:   {final_rate:.3f}")
    print(f"Profit/Loss (£): {profit:.2f}")

    # daily volatility
    daily_vol_est = df["Return"].std()

    # annualized (≈ 252 trading days per year)
    annualized_vol = daily_vol_est * np.sqrt(252)

    print(f"Estimated daily vol: {daily_vol_est:.3%}")
    print(f"Annualized vol: {annualized_vol:.2%}")

    return df


def plot_fx(df: pd.DataFrame):
    plt.figure(figsize=(10, 4))
    plt.plot(df["Day"], df["FX_Rate"])
    plt.title("Simulated GBP/USD Exchange Rate")
    plt.xlabel("Day")
    plt.ylabel("FX Rate")
    plt.grid(True)
    plt.show()
