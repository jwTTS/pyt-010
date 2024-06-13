"""
Demo for PCA and Optimization
"""

# %% Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from scipy.stats import norm
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint

# %% Optimization (Minimization)
# Used in portfolio optimization

def optw(w, *args):
    return(np.matmul(np.matmul(w,V),w))

np.random.seed(42)
n = 60 #number of observations
m = 25 #number of assets

simrtns = np.zeros((n,m))

for i in range(1, 6): #loop over means
    for j in range(1, 6): #loop over std
        for k in range(0, simrtns.shape[0]): #loop over rows
            simrtns[k, ((5*(i-1))+(j-1))] = np.random.normal(i,j) #how to skip looping through rows?

V = np.cov(simrtns, rowvar=False)
mu = np.mean(simrtns, axis=0)

# Set initial values for the weights and define the expected return
w = np.matrix([0.04] * 25).T
expect_return = 5

# Weight constraint
A = np.matrix([1]*25)
constraint_1 = LinearConstraint(A, 1, 1)

# for the return constraint, the asset returns are the coefficients
constraint_2 = LinearConstraint(mu, expect_return, np.inf)

weight = minimize(optw, w, (V), constraints=(constraint_1,constraint_2), options={'maxiter':1000})

weights = []

for expect_return in np.linspace(1,10, 20):
    constraint_2 = LinearConstraint(mu, expect_return, np.inf)
    weight = minimize(optw, w, (V), constraints=(constraint_1,constraint_2), options={'maxiter':1000})
    if weight.success == True:
        weights.append(weight.x)

# Find the portfolio returns and variances
portmu = []
portvar = []

for w in weights:
    portmu.append(w @ mu)
    portvar.append(w @ V @ w)

portstd = np.sqrt(portvar)

plt.plot(portstd, portmu)
plt.title('Portfolio Frontier')
plt.xlim([0,1.25])
plt.ylim([0,11])
plt.xlabel('Portfolio Risk')
plt.ylabel('Portfolio Expected Return')
plt.show()

# %% Principle Component Analysis
# Used in creating factors from a portfolio
# Example using simulated data, 25 assets, with 5 factors

np.random.seed(42)
n = 60 #number of observations
m = 25 #number of assets

simrtns = np.zeros((n,m))

for i in range(1, 6): #loop over means
    for j in range(1, 6): #loop over std
        for k in range(0, simrtns.shape[0]): #loop over rows
            simrtns[k, 5*(i-1)+j-1] = np.random.normal(i,j) #how to skip looping through rows?

princomp = PCA().fit(simrtns)

# What do we have returned?
princomp.components_

princomp.explained_variance_ratio_
sum(princomp.explained_variance_ratio_[:5])

comp = princomp.components_.T
# Taking the transpose so that each column 
# are the factor "weights" for each asset (matrix multiplication row by column)

# You can think of it that each column is an factor
# the rows are the weights of the asset to generate that factor

# We can see how much of the variance in returns is explained by
# each factor. Sum to one.

# Unfortuantely we cannot just use the transform method, because it demeans the data
# which we don't want. So lets do it manually
# Scale the componets to sum to one (weights)

scale = np.sum(comp, axis=0) 
import numpy.matlib
scales = np.matlib.repmat(scale, 25, 1)

scaled_comp = comp/scales

factors = np.matmul(simrtns ,scaled_comp)

factors.shape
factors

# Let's have a quick look at the R2 for the regressions
for i in range(1,25):
    tempols = sm.OLS(simrtns[ : , i], factors[ : , :5]).fit()
    print(tempols.rsquared_adj)

# We can see that they are heavily loaded towards the high variance
# assets, which makes sense because that is how PCA works