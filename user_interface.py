"""
Module containing the UserInterface class. This class collects the user input by displaying some texts in the terminal and prompts the user for their input. 
"""

from real_world_data import RealWorldData
import yfinance as yf

class UserInterface:
   """
   Class containing the methods required to collect all necessary information from the user for stock, type of option and moneyness of the option they want. 
   Contains only static methods as this class will not be instantiated. 
   """

   @staticmethod
   def get_user_inputs():
      """
      Method that brings functionality together and calls other methods in class to collect user input. 

      Returns:
         inputs_dict (dict): Dictionary containing all user input and other data needed for the application. 
      """
      print("=" * 50)
      print("Welcome to our Binomial Option Pricing Application.")
      print("=" * 50)

      ticker = UserInterface._get_ticker()
      option_type = UserInterface._get_option_type()
      strike = UserInterface._get_strike(ticker, option_type)

      data = RealWorldData()
      S0 = data.get_current_price(ticker)
      vol = data.get_volatility(ticker)
      R = data.get_rf("^IRX")

      inputs_dict = {
         "ticker": ticker,
         "S0": S0,
         "K": strike, 
         "T": 1,
         "R": R,
         "sigma": vol,
         "n_steps": 10,
         "option_type": option_type
      }

      return inputs_dict


   @staticmethod
   def _get_ticker():
      """
      Private method that prompts the user to input the ticker of the stock. 

      Returns:
         ticker (str): The ticker input by the user. 
      """
      print("\nPlease enter the stock ticker symbol (e.g. NVDA, TSLA, JNJ): ")
      while True:
         ticker_input = input("> ").upper().strip()
         if not UserInterface._validate_ticker(ticker_input):
            print("This ticker does not exist. Please enter a valid Ticker.")
         else:
            return ticker_input
      

   @staticmethod
   def _validate_ticker(ticker):
      """
      Private method that ensures the ticker exists. 

      Parameter: 
         ticker (str): The ticker of the stock. 
      
      Returns:
         bool: True if the ticker exists, False otherwise. 
      """
      #Method to check if ticker exists found on Stack Overflow
      info = yf.Ticker(ticker).history(period = "7d", interval = "1d")
      return len(info) > 0


   @staticmethod
   def _get_option_type():
      """
      Private method which prompts the user to input the type of option they want to price. 

      Returns:
         option_type (str): The type of option. 
      """
      print("\nChoose option type:")
      print("1. Call option")
      print("2. Put option\n")
      print("Enter 1 or 2:\n")

      while True:
         choice = input("> ").strip()
         if choice == "1":
            return "call"
         elif choice == "2":
            return "put"
         print("Invalid choice! Please enter 1 or 2.")
   
   @staticmethod
   def _get_strike(ticker, option_type):
      """
      Private method that prompts the user to choose the moneyness of the option they want to price. 

      Parameters:
         ticker (str): The ticker of the stock who's option is being priced. 
         option_type (str): Type of option being pricer. Call or Put. 

      Returns:
         strike (float): The strike price of the option at chosen moneyness. 
      """
      print("\nSelect the moneyness of the option (strike price relative to current price):")
      print("1. ATM - At The Money (Strike close to current price)")
      print("2. ITM - In The Money (Favourable strike)")
      print("3. OTM - Out The Money (Unfavourable strike)\n")
      print("Enter your choice as 1-3:\n")

      data = RealWorldData()

      while True:
         choice = input("> ").strip()

         if choice == "1":
            strike = data.get_atm_strike(ticker)
            return strike
         elif choice == "2":
            itm_call, itm_put = data.get_itm_strike(ticker, percent_itm=10)
            strike = 0
            if option_type == "call":
               strike = itm_call
            else:
               strike = itm_put
            return strike
         elif choice == "3":
            otm_call, otm_put = data.get_otm_strike(ticker, percent_otm=10)
            if option_type == "call":
               strike = otm_call
            else:
               strike = otm_put
            return strike
         
         print("Invalid choice! Please enter a number between 1 and 3.\n")

      