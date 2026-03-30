"""
Module containing class to show the put-call parity between put and call options and to show the historical stock price. 
"""

import numpy as np
import matplotlib.pyplot as plt
from black_sholes_merton_pricer import BlackSholes
from real_world_data import RealWorldData


class Visual:
   """
   A visualisation for analysing stock prices and options:

   Attributes:
   S0 (float): Initial Stock Price.
   K (float): Strike Price.
   T (float): Time to expiry (in years).
   R (float): Risk-free interest rate.
   vol (float): Historical volatility of the stock.
   ticker_input (float): Ticker of the stock.
   data (RealWorldData): Instance of RealWorldData class to be able to fetch real world data of the stock. 
   """
   def __init__(self, S0: float, R: float, vol: float, T: float, K: float, ticker_input: str):
      """
      Method to initialise the visualisation class. 

      Parameters
         S0 (float): Initial price of stock.
         R (float): Risk free rate. 
         vol (float): Historical volatility of the stock.
         T (float): Time till expiry. 
         K (float): Strike price of stock. 
         ticker_input (str): Ticker of the stock. 
      """
      self.R = R
      self.S0 = S0
      self.vol = vol
      self.T = T
      self.K = K
      self.data = RealWorldData()
      self.ticker_input = ticker_input

   def plt_put_call_prices(self):
      """
      Computes the price of put and call options on a given stock and then plots the two against each other, showing the put call parity. Also disaplay historical stock prices. 
      """
      S0_range = np.linspace(self.S0*0.6,self.S0*1.4, num= 100)

      pricer_bs_call = BlackSholes(S0 = self.S0, K=self.K, T=self.T, R = self.R, option_type="call", vol=self.vol)
      pricer_bs_put = BlackSholes(S0 = self.S0, K=self.K, T=self.T, R = self.R, option_type="put", vol=self.vol)

      price_series_put = []
      price_series_call = []
      df = self.data.get_df(self.ticker_input)

      for S in S0_range:
         pricer_bs_call.S0 = S
         pricer_bs_put.S0 = S

         price_call = pricer_bs_call.compute_blackscholes()
         price_put = pricer_bs_put.compute_blackscholes()

         price_series_call.append(price_call)
         price_series_put.append(price_put)

      #To plot both graphs, first option one and second stock prices
      fig, axes = plt.subplots(1, 2, figsize=(14, 6))
      fig.suptitle(f'Black-Scholes option analysis', fontsize=14, y=1.05)

      ax1 = axes[0]
      ax1.plot(S0_range, price_series_call, label='BSM Price Call')
      ax1.plot(S0_range, price_series_put, label='BSM Price Put')
      ax1.legend()
      ax1.set_title(f'Option prices of {self.ticker_input}')
      ax1.set_xlabel('Stock price')
      ax1.set_ylabel('Option price')
      
      ax2 = axes[1]
      ax2.plot(df['Date'], df['Close'], label=f'{self.ticker_input}')
      ax2.plot(df['Date'], df['80MA'], label='80MA')
      ax2.legend()
      ax2.set_title(f'Stock Price of {self.ticker_input}')
      ax2.set_xlabel('Time')
      ax2.set_ylabel('Stock price')

      plt.show()
      return ax1, ax2