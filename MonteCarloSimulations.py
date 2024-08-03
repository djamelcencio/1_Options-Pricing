#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt

class MonteCarloSimulations:
    def __init__(self, s0, expiry, nbr_sim, time_step, sigma, rfr):
        # stock price at time 0 = 100 in this case
        self.s0 = s0
        # time to expiry
        self.expiry = expiry
        # the number of simulations (we will vary this parameter)
        self.nbr_sim = nbr_sim
        # the number of time step (we will vary this parameter)
        self.time_step = time_step
        # volatility (we will vary this parameter)
        self.sigma = sigma
        # risk free rate (we will vary this parameter)
        self.rfr = rfr
        

    def get_paths(self):
        
        all_paths = [] # list where we will store all simulations i.e. all paths
        delta_t = self.expiry/self.time_step # dt size when expiry = 1 and time_step = 252 --> dt = 1 business day
        
        # for each path, each simulation
        for i in range(self.nbr_sim):
            one_path = [] # list to store each path i.e. each simulation
            one_path_start = self.s0 # each simulation starts from s0, by default = 100
            one_path.append(one_path_start) # this initial value is stored as the first value of each path
            
            # for each time step
            for j in range(self.time_step):
                # Brownian motion formula in discrete time
                one_path_after = one_path_start * (1 + self.rfr * delta_t + self.sigma * np.sqrt(delta_t) * np.random.normal(0, 1))
                one_path_start = one_path_after # replacing the initial value with the new random value at each step, so it does not start from 100 each time, but from the new random value
                one_path.append(one_path_after) # appending each step to the one_path list
            
            all_paths.append(one_path) # storing each full random path to the all_paths lists
            
        return all_paths

    def plot_paths(self, all_paths):
        plt.figure(figsize=(10, 6))
        for path in all_paths:
            plt.plot(path)
        plt.title('Monte Carlo Simulation Paths')
        plt.xlabel('Time Step')
        plt.ylabel('Stock Price')
        plt.grid(True)
        plt.show()

# Example usage
#mc_sim = MonteCarloSimulations(s0=100, expiry=1, nbr_sim=100, time_step=252, sigma=0.2, rfr=0.05)
#paths = mc_sim.get_paths()
#mc_sim.plot_paths(paths)


# In[ ]:




