# Option Pricing Application

A python application that prices European options using both the Binomial Tree model and the Black-Scholes-Merton mode, with real-world market data integration. 

# My Contribution
BinomialModelSimulation was implemented in file binomial_simulation.py to:
Construct stock price tree under up/down moves
Generate all future price states
Plot tree structure to illustrate path dependence
Visualize how step size affects state distribution

### Prerequisites
- Python 3.8 or higher
- pip (to install packages)

### Step 1: 
Clone the repository

### Step 2:
Open a terminal in the project directory and run:
```bash
pip install numpy scipy matplotlib yfinance
```

### Step 3:
Navigate to the ```source``` directory

### Step 4:
In the terminal run:
```bash
python3 main.py
```