"""
Binomial option pricing class.  
"""

import numpy as np

class BinomialOptionPricer:
   """
   Binomial option pricer supporting European.  
   
   Attributes:
      S0: Initial Stock Price
      K: Strike Price
      T: Time to expiry (in years)
      R: Risk-free interest rate
      n_steps: Number of steps in the binomial tree
      option_type: Either a Call option or a Put option
      sigma: (Optional) volatility
   """

   def __init__(self, S0: float,K: float, T: float, R: float, n_steps: int, option_type: str, sigma: float):
      """
      Initialize the Binomial Option Pricer class.

      Parameters:
         S0 (float): Initial price of stock.
         K (float): Strike price of stock. 
         T (float): Time till expiry. 
         R (float): Risk free rate. 
         n_steps (int): Number of steps in the binomial tree. 
         option_type (str): Type of option being priced. Either Call or Put. 
         sigma (float): Historical volatility of the stock.
      """
      self.S0 = S0
      self.K = K
      self.T = T
      self.R = R
      self.n_steps = n_steps
      self.option_type = option_type.lower()
      self.sigma = sigma

      self.compute_parameters()


   def compute_parameters(self) -> None:
      """
      Compute the additional non-standard parameters for the binomial model and set the appropriate attributes. 
      """
      self.dt = self.T / self.n_steps

      self.R = np.exp(self.R * self.T/self.n_steps) - 1

      self.up = np.exp(self.sigma * np.sqrt(self.dt))  
      self.down = 1 / self.up  

      #Risk Neutral probabilities
      self.qu = (1 + self.R - self.down) / (self.up - self.down)
      self.qd = 1 - self.qu

   def build_stock_value_tree(self):
      """
      Builds binomial tree for price of stock going forward.

      Return:
         List[List]: 2D list representing the stock price tree
      """
      tree = []
      for _ in range(self.n_steps + 1):
         tree.append([0.0] * (self.n_steps + 1))

      for t in range(1,self.n_steps + 2):
         for k in range(t):
            #Now we compute the u^k * d^(t-1-k) * S0
            stock_value = self.up ** k * self.down ** (t-k-1) * self.S0
            tree[t-1][k] = stock_value

      return tree

   def price_european(self):
      """
      Computes the price of a european option using backward induction. 

      Returns:
         List[List]: 2D array of discounted option price at each timestep.  
      """
      stock_tree = self.build_stock_value_tree()

      #Make the tree for the price of the option
      option_tree = []
      for _ in range(self.n_steps + 1):
         option_tree.append([0.0] * (self.n_steps + 1))
      
      #Compute payoff at expiration
      for k in range(self.n_steps + 1):
         stock_price = stock_tree[self.n_steps][k]
         if self.option_type == 'call':
            option_tree[self.n_steps][k] = max(stock_price - self.K, 0)
         else:
            option_tree[self.n_steps][k] = max(self.K - stock_price, 0)

      #Now go backwards with the values from terminal payoff
      for t in range(self.n_steps -1, -1, -1):
         #Go from the back down to 0
         for k in range(t + 1):
            up_value = option_tree[t + 1][k + 1]
            down_value = option_tree[t + 1][k]
            option_tree[t][k] = (self.qu * up_value + self.qd * down_value) / (1 + self.R)
   
      return option_tree