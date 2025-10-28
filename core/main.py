from core.bond_pricer import bond_duration, price_bond, simulate_rate_sensitivity
from core.fx_simulator import plot_fx, simulate_fx_path
from core.risk_engine import plot_portfolio_sensitivity, portfolio_risk_summary
from core.scenario_engine import plot_scenario_results, simulate_scenarios
from core.var_engine import monte_carlo_var

df = simulate_scenarios()
print(df)
plot_scenario_results(df)
df = simulate_fx_path(start_rate=1.25, days=200, daily_vol=0.006)
print(df.head())
plot_fx(df)

df = simulate_rate_sensitivity()
print(df.head())


dur = bond_duration()
print(f"Modified Duration ≈ {dur:.2f} years")

# DV01: change in price for 1bp (0.0001) rate move
base = price_bond()
up = price_bond(market_rate=0.0501)
dv01 = base - up
print(f"DV01 ≈ £{dv01:.4f}")
print(portfolio_risk_summary())

plot_portfolio_sensitivity()

summary, pnl = monte_carlo_var()
print(summary)
