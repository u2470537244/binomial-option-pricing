"""
Black Scholes option pricing class. 
"""
import numpy as np
from scipy import stats

class BlackSholes:
   """
   Black-Scholes-Merton model for pricing European options. Underlying stock does not pay dividends. 
   
   Attributes:
   S0 (float): Initial Stock Price
   K (float): Strike Price
   T (float): Time to expiry (in years)
   R (float): Risk-free interest rate
   vol (float): Historical volatility of the stock
   option_type (str): Either a Call option or a Put option
   """
   def __init__(self, S0:float, K:float, T:float, R:float, vol:float, option_type: str):
      """
      Initialize Black-Scholes pricer. 
      
      Parameters:
         S0 (float): Initial price of stock.
         K (float): Strike price of stock. 
         T (float): Time till expiry. 
         R (float): Risk free rate. 
         vol (float): Historical volatility of the stock.
         option_type (str): Type of option being priced. Either Call or Put. 
      """
      self.S0 = S0
      self.K = K
      self.T = T
      self.vol = vol
      self.R =R
      self.option_type = option_type.lower()
   
   def _compute_d1(self):
      """
      Method that computes the value of d1. 

      Returns:
         d1 (float): Computed d1 value.
      """
      return (np.log(self.S0/self.K) + (self.R + self.vol**2 / 2) * self.T)/(self.vol * np.sqrt(self.T))
   
   def _compute_d2(self):
      """
      Method that computes the value of d2. 

      Returns:
         d2 (float): Computed d2 value. 
      """
      d1 = self._compute_d1()
      return d1 - self.vol * np.sqrt(self.T)

   def compute_blackscholes(self):
      """
      Compute the price of the european option according to the BSM. 

      Returns:
         option_price (float): The price of the option. 
      """
      if self.option_type=="call":
         return self.S0 * stats.norm.cdf(self._compute_d1()) - self.K * np.exp(-self.R * self.T) * stats.norm.cdf(self._compute_d2())

      elif self.option_type=="put":
         return self.K * np.exp(-self.R * self.T) * stats.norm.cdf(-self._compute_d2()) - self.S0 * stats.norm.cdf(-self._compute_d1())


