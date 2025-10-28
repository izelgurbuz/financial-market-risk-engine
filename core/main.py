from core.var_engine import monte_carlo_var

# df = simulate_fx_path(start_rate=1.25, days=200, daily_vol=0.006)
# print(df.head())
# plot_fx(df)

# df = simulate_rate_sensitivity()
# print(df.head())


# dur = bond_duration()
# print(f"Modified Duration ≈ {dur:.2f} years")

# # DV01: change in price for 1bp (0.0001) rate move
# base = price_bond()
# up = price_bond(market_rate=0.0501)
# dv01 = base - up
# print(f"DV01 ≈ £{dv01:.4f}")
# print(portfolio_risk_summary())

# plot_portfolio_sensitivity()

summary, pnl = monte_carlo_var()
print(summary)
