 # Ignore Warnings
import warnings
warnings.filterwarnings('ignore')

# Import Pandas, Numpy and Scipy
import pandas as pd
import numpy as np
from scipy.stats import norm
import math
from scipy.stats import norm
import networkx as nx

# Import plotly express
import plotly.express as px
import plotly.graph_objects as go
px.defaults.width, px.defaults.height = 1000, 600
import matplotlib.pyplot as plt

 # Create a user defined function
def binomial_option(spot: float, strike: float, rate: float, sigma: float, time: float, steps: int, output: int=0):
    
    # params
    ts = time/steps
    u = 1+sigma*math.sqrt(ts)
    v = 1- sigma*math.sqrt(ts)
    p = 0.5+rate*math.sqrt(ts)/(2*sigma)
    df = 1/(1+rate*ts)
    
    # initialize arrays
    px = np.zeros((steps+1, steps+1))
    cp = np.zeros((steps+1, steps+1))
    V = np.zeros((steps+1, steps+1))
    d = np.zeros((steps+1, steps+1))
    
    # binomial loop
    
    # forward loop
    for j in range(steps+1):
        for i in range(j+1):
            px[i,j] = spot*np.power(v,i)*np.power(u,j-i)
            cp[i,j] = np.maximum(px[i,j]-strike, 0)
            
   # reverse loop
    for j in range(steps+1, 0, -1):
        for i in range(j):
            if (j==steps+1):
                V[i,j-1] = cp[i,j-1]
                d[i,j-1] = 0
            else:
                V[i,j-1] = df*(p*V[i,j]+(1-p)*V[i+1,j])
                d[i,j-1] = (V[i,j]-V[i+1,j])/(px[i,j]-px[i+1,j])
                
    results = np.around(px,2), np.around(cp,2), np.around(V,2), np.around(d,4)
    
    return results[output]



# Define the start and end of volatility values
start = 0.05
end = 1.0

# Define the step size
step = 0.01

volatility = [start + i * step for i in range(int((end - start) / step) + 1)]

my_dict_1 = {}

for x in volatility:
    opx = binomial_option(100,100,0.05,x,1,4,2)
    my_dict_1[x] = opx[0,0]

# Extract keys and values
vol = list(my_dict_1.keys())
opt_val = list(my_dict_1.values())

# Plot
plt.figure(figsize=(8, 6))
plt.scatter(vol, opt_val)
plt.xlabel('Volatility')
plt.ylabel('Options Value')
plt.title('Volatility vs Options Value')
plt.show()

# Define the start and end of number of steps 
start = 4
end = 50

steps = [x for x in range(start, end+1)]

my_dict_2 = {}

for x in steps:
    opx = binomial_option(100,100,0.05,0.2,1,x,2)
    my_dict_2[x] = opx[0,0]

# Extract keys and values
nbr_steps = list(my_dict_2.keys())
opt_val = list(my_dict_2.values())

# Plot
plt.figure(figsize=(8, 6))
plt.scatter(nbr_steps, opt_val)
plt.xlabel('Number of steps')
plt.ylabel('Options Value')
plt.title('Number of steps vs Options Value')
plt.show()


