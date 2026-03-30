"""
Module containing the Converge Analyser class. Used to see how the Binomial Option Pricer's price converges to the Black-Scholes model's price as steps increase. 
"""

from black_sholes_merton_pricer import BlackSholes
from binomial_option_pricer import BinomialOptionPricer
import matplotlib.pyplot as plt

class ConvergenceAnalyser:
   """
   Displays a visualisation of how the Binomial Option Pricer's calculated price converges to the one calculated by the Black-Scholes model.  
   """
   @staticmethod
   def check_convergence(S0, K, T, R, sigma, option_type, max_steps=200, step_increment=5):
      """
      Computes binomial option price for different steps and creates a visualisation to show how the price converges to Black-Scholes price. 

      Parameters:
         S0 (float): Initial price of stock.
         K (float): Strike price of stock. 
         T (float): Time till expiry. 
         R (float): Risk free rate. 
         sigma (float): Historical volatility of the stock.
         option_type (str): Type of option being priced. Either Call or Put. 
         max_steps (int): Maximum number of steps that the Binomial Option Pricer will use to compute the price. 
         step_increment (int): Increaser in steps for each iteration of computing the option's price. 
      """
      pricer_bs = BlackSholes(S0, K, T, R, sigma, option_type)
      bs_price = pricer_bs.compute_blackscholes()

      steps = list(range(1, max_steps, step_increment))
      binomial_prices = []
      for n in steps:
         pricer = BinomialOptionPricer(S0, K, T, R, n, option_type, sigma)
         price = pricer.price_european()[0][0]
         binomial_prices.append(price)
      
      plt.figure(figsize=(14,6))
      plt.plot(steps, binomial_prices, label=f"Binomial Price: ${binomial_prices[len(binomial_prices)-1]:.2f}")
      plt.axhline(y=bs_price, color = 'r', label =f"Black Scholes Price: ${bs_price:.2f}")
      plt.xlabel("Number of steps in binomial tree")
      plt.ylabel("Option Price")
      plt.title("Convergence of Binomial model to Black Scholes")
      plt.legend()
      plt.show(block=False)