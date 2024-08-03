import numpy as np
import scipy.stats as sp

class PricingSimulatedLookback:
    def __init__(self, spot, strike,rate, sigma, time, sims, steps):
        self.spot = spot
        self.strike = strike
        self.rate = rate
        self.sigma = sigma
        self.time = time
        self.sims = sims
        self.steps = steps
        self.dt = self.time / self.steps
        
    def Simulations(self):
        
        total = np.zeros((self.sims,self.steps+1),float)
        pathwiseS= np.zeros((self.steps+1),float)
        
        for j in range(self.sims):
            pathwiseS[0] =self.spot
            total[j,0] = self.spot
            for i in range(1,self.steps+1):
                phi = np.random.normal()
                pathwiseS[i] = pathwiseS[i-1]*(1+self.rate*self.dt+self.sigma*phi*np.sqrt(self.dt))
                total[j,i]= pathwiseS[i]
            
        return total.reshape(self.sims, self.steps+1)

    def CallFloatingStrike(self):
        
        getpayoff = self.Simulations()
        minprice = np.zeros((self.sims),float)
        priceatmaturity = np.zeros((self.sims),float)
        callpayoff = np.zeros((self.sims),float)
        for j in range(self.sims):
            minprice[j] = min(getpayoff[j,])
            priceatmaturity[j] = getpayoff[j,self.steps-1]
            callpayoff[j] = max(priceatmaturity[j]-minprice[j],0)
        
        return np.exp(-self.rate*self.time)*np.average(callpayoff)

    def PutFloatingStrike(self):
        
        getpayoff = self.Simulations()
        maxprice = np.zeros((self.sims),float)
        priceatmaturity = np.zeros((self.sims),float)
        Putpayoff = np.zeros((self.sims),float)
        for j in range(self.sims):
            maxprice[j] = max(getpayoff[j,])
            priceatmaturity[j] = getpayoff[j,self.steps-1]
            Putpayoff[j] = max(maxprice[j]-priceatmaturity[j],0)
        
        return np.exp(-self.rate*self.time)*np.average(Putpayoff)
    
    def CallFixedStrike(self):
        
        getpayoff = self.Simulations()
        maxprice = np.zeros((self.sims),float)
        callpayoff = np.zeros((self.sims),float)
        for j in range(self.sims):
            maxprice[j] = max(getpayoff[j,])
            callpayoff[j] = max(maxprice[j]-self.strike,0)
        
        return np.exp(-self.rate*self.time)*np.average(callpayoff)
    
    def PutFixedStrike(self):
        
        getpayoff = self.Simulations()
        minprice = np.zeros((self.sims),float)
        Putpayoff = np.zeros((self.sims),float)
        for j in range(self.sims):
            minprice[j] = min(getpayoff[j,])
            Putpayoff[j] = max(self.strike-minprice[j],0)
        
        return np.exp(-self.rate*self.time)*np.average(Putpayoff)

