import pandas as pd
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt

class Simulations_Asian:
    def __init__(self, all_simulations, rfr, expiry, option_type, \
                 sample_window = None, strike = None):
        # all_simulations are all random paths 
        self.all_simulations = all_simulations
        # option type 'call' or 'put'
        self.option_type = option_type
        # risk-free rate
        self.rfr = rfr
        # expiry
        self.expiry = expiry
        # Strike is None by default since there are some floating situations
        self.strike = strike
        # sample_window for discrete sampling
        self.sample_window = sample_window
        
    def discrete_fix_arith(self):
        # DISCRETE SAMPLING - ARITHMETIC AVERAGE - FIXED STRIKE
        
        discrete_sample_index = [i for i in range(len(self.all_simulations)) if i%self.sample_window == 0] #only keep indices that are multiple of the sample_window 
        discrete_sample_data = self.all_simulations.iloc[discrete_sample_index] #only keep data points of the random walk that corresponds to those indices
        
        A = discrete_sample_data.mean() #get the mean of each simulation discretely sampled based on the sample window
        
        # if we are dealing with a call option
        # if the call option is "in the money", the pay-off is the maximum of each average (of each simulation) minus the strike price or 0 ("out of the money" call option)
        # the call  option is then present-valued 
        # finally we get the expected value of the present-valued pay-off by simply returning the mean. 
        # we do the same for the put, but we are just changing the pay-off function. 
        if self.option_type == 'call': 
            payoff = A.apply(lambda x: max(x - self.strike, 0)*\
                             np.exp(-self.rfr*self.expiry))
            
            # std_error = np.std(discrete_sample_data)/sqrt(100)
            
            return payoff.mean()
        
        elif self.option_type == 'put':
            payoff = A.apply(lambda x: max(self.strike - x, 0)*\
                             np.exp(-self.rfr*self.expiry))
            return payoff.mean()
        
    def discrete_fix_geo(self):
        # DISCRETE SAMPLING - GEOMETRIC AVERAGE - FIXED STRIKE

        discrete_sample_index = [i for i in range(len(self.all_simulations)) if i%self.sample_window == 0]
        discrete_sample_data = self.all_simulations.iloc[discrete_sample_index]
        
        # We just change the average function and use a geometric average instead of an arithmetic one
        A = discrete_sample_data.apply(lambda x: gmean(x))
        
        if self.option_type == 'call':
            payoff = A.apply(lambda x: max(x - self.strike, 0)*\
                             np.exp(-self.rfr*self.expiry))
            return payoff.mean()
        
        elif self.option_type == 'put':
            payoff = A.apply(lambda x: max(self.strike - x, 0)*\
                             np.exp(-self.rfr*self.expiry))
            return payoff.mean()
        
    def discrete_floating_arith(self):
        # DISCRETE SAMPLING - ARITHMETIC AVERAGE - FLOATING STRIKE

        discrete_sample_index = [i for i in range(len(self.all_simulations)) if i%self.sample_window == 0]
        discrete_sample_data = self.all_simulations.iloc[discrete_sample_index]
        
        # We keep the same artithmetic average...
        A = discrete_sample_data.mean()
        
        # ...but we change the pay-off function 
        # The strike price is not fixed, but is the last value of each random process.
        if self.option_type == 'call':
            payoff = (A - discrete_sample_data.iloc[-1,:]).apply(lambda x: max(x, 0))
            return payoff.mean()
        
        elif self.option_type == 'put':
            payoff = (discrete_sample_data.iloc[-1,:] - A).apply(lambda x: max(x, 0))
            return payoff.mean()
        
    def discrete_floating_geo(self):
        # DISCRETE SAMPLING - GEOMETRIC AVERAGE - FLOATING STRIKE

        discrete_sample_index = [i for i in range(len(self.all_simulations)) if i%self.sample_window == 0]
        discrete_sample_data = self.all_simulations.iloc[discrete_sample_index]
        
        A = discrete_sample_data.apply(lambda x: gmean(x))
        
        if self.option_type == 'call':
            payoff = (A - discrete_sample_data.iloc[-1,:]).apply(lambda x: max(x, 0))
            return payoff.mean()
        
        elif self.option_type == 'put':
            payoff = (discrete_sample_data.iloc[-1,:] - A).apply(lambda x: max(x, 0))
            return payoff.mean()
        
    def continuous_fix_arith(self):
        # CONTINUOUS SAMPLING - ARITHMETIC AVERAGE - FIXED STRIKE

        A = self.all_simulations.mean()
        
        if self.option_type == 'call':
            payoff = A.apply(lambda x: max(x - self.strike, 0)*\
                             np.exp(-self.rfr*self.expiry))
            return payoff.mean()
        
        elif self.option_type == 'put':
            payoff = A.apply(lambda x: max(self.strike - x, 0)*\
                             np.exp(-self.rfr*self.expiry))
            return payoff.mean()
        
        
    def continuous_fix_geo(self):
        # CONTINUOUS SAMPLING - GEOMETRIC AVERAGE - FIXED STRIKE

        A = self.all_simulations.apply(lambda x: gmean(x))
        
        if self.option_type == 'call':
            payoff = A.apply(lambda x: max(x - self.strike, 0)*\
                             np.exp(-self.rfr*self.expiry))
            return payoff.mean()
        
        elif self.option_type == 'put':
            payoff = A.apply(lambda x: max(self.strike - x, 0)*\
                             np.exp(-self.rfr*self.expiry))
            return payoff.mean()
        
    def continuous_floating_arith(self):
        # CONTINUOUS SAMPLING - ARITHMETIC AVERAGE - FLOATING STRIKE

        A = self.all_simulations.mean()
        
        if self.option_type == 'call':
            payoff = (A - self.all_simulations.iloc[-1,:]).apply(lambda x: max(x, 0))
            return payoff.mean()
        
        elif self.option_type == 'put':
            payoff = (self.all_simulations.iloc[-1,:] - A).apply(lambda x: max(x, 0))
            return payoff.mean()

    def continuous_floating_geo(self):
        # CONTINUOUS SAMPLING - GEOMETRIC AVERAGE - FLOATING STRIKE

        A = self.all_simulations.apply(lambda x: gmean(x))
        
        if self.option_type == 'call':
            payoff = (A - self.all_simulations.iloc[-1,:]).apply(lambda x: max(x, 0))
            return payoff.mean()
        
        elif self.option_type == 'put':
            payoff = (self.all_simulations.iloc[-1,:] - A).apply(lambda x: max(x, 0))
            return payoff.mean()

