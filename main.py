from binomial_option_pricer import BinomialOptionPricer
from black_sholes_merton_pricer import BlackSholes
from visualizations import Visual
from user_interface import UserInterface
from convergence_analyser import ConvergenceAnalyser
from binomial_simulation import BinomialModelSimulation
inputs = UserInterface.get_user_inputs()

pricer_bt = BinomialOptionPricer(
   S0 = inputs["S0"], K=inputs["K"], T=inputs["T"], R = inputs["R"], n_steps = inputs["n_steps"], option_type=inputs["option_type"], sigma=inputs["sigma"]
)

pricer_bs = BlackSholes(
   S0 = inputs["S0"], K=inputs["K"], T=inputs["T"], R = inputs["R"], option_type=inputs["option_type"], vol=inputs["sigma"]
)

price_bs = pricer_bs.compute_blackscholes()
option_tree = pricer_bt.price_european()

print(f"The final option price by the Binomial Model is: {option_tree[0][0]:.4f}")
print(f"The final option price by the Black Scholes Model is: {price_bs:.4f}")

ConvergenceAnalyser.check_convergence(S0 = inputs["S0"], K=inputs["K"], T=inputs["T"], R = inputs["R"], sigma=inputs["sigma"], option_type=inputs["option_type"], max_steps=200, step_increment=5)

vis = Visual(S0 = inputs["S0"], K=inputs["K"], T=inputs["T"], R = inputs["R"], vol=inputs["sigma"], ticker_input=inputs["ticker"])
vis.plt_put_call_prices()
BinomialModelSimulation(pricer_bt).plot_stock_tree()