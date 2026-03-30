import matplotlib.pyplot as plt
import numpy as np
from real_world_data import RealWorldData
from binomial_option_pricer import BinomialOptionPricer as BOP
class BinomialModelSimulation:
    def __init__(self, ticker:BOP):
        self.ticker = ticker
        
    def get_stock_tree(self)->list:
        lst = list()
        for i in range(0,self.ticker.n_steps):
            lst.append([])
        for i in range(0,self.ticker.n_steps):
            for up_count in range(0,i+1):#from 0 to i
                down_count = i-up_count
                stock_value = self.ticker.S0*(self.ticker.up**up_count)*(self.ticker.down**down_count)
                lst[i].append(stock_value)
        return lst

    # def plot(self):
    #     plt.subplots(figsize=(10, 6))
    #     plt.plot([2,4],[33,34.2])
    #     plt.show()
# # Parameters
# n = 4  # Number of steps
# S0 = 100  # Initial stock price
# u = 1.1  # Up factor
# d = 0.9  # Down factor


    def plot_stock_tree(self):
        # Plot the tree
        ad,ax = plt.subplots(figsize=(10, 6))
        tree = self.get_stock_tree()
        for timeStamp in range(self.ticker.n_steps-1):
            for j in range(timeStamp+1):
                ax.plot([timeStamp, timeStamp+1], [tree[timeStamp][j],tree[timeStamp+1][j+1]])  # Plot the up
                ax.plot([timeStamp, timeStamp+1], [tree[timeStamp][j],tree[timeStamp+1][j]])    # Plot the down

        # Set labels and title
        ax.set_xlabel('Steps')
        ax.set_ylabel('Stock Price')
        ax.set_title('Binomial Model: Stock Price Evolution')

        # # Show grid and plot
        # ax.grid(True)
        # plt.tight_layout()

        plt.show()
# test
#     def plotSample():
#         pricer_ss=BOP(
#             S0=100,
#             n_steps=7,
#             K=120,
#             T=4,
#             R=0.05,
#             option_type="European put",
#             sigma=0.6
#         )
#         bms=BinomialModelSimulation(pricer_ss)
#         print(bms.get_stock_tree())
#         bms.plot_stock_tree()
# #BinomialModelSimulation.plotSample()
