"""
Python Programming - Assignment 1 Solutions
"""
import numpy as np

#%% Exercise 1
#Cast the operation to an integer
j=4.3
k=5.5
i = int(j * k)
print(i)
print(j*k) #What do you notice about the behaviour?
# The decimals are chopped off
print(type(i))
################################################################

#%% Exercise 2
#Convert string $123,456,789 into a useable integer
deal_value = '$123,456,789'
deal_value = deal_value.strip('$')
deal_value = ''.join(i for i in deal_value.split(','))
deal_value = int(deal_value)
print(deal_value)
print(type(deal_value))
print(deal_value * 2)
################################################################

#%% Exercise 3

mylist = [100,99,105,110,95,102]
for price in mylist:
    output = "Price is ${} {}"
    if price > 102:
        # print("Price is $" + str(price) + " Sell")
        print(output.format(price,"Sell"))
    elif price < 100:
        # print("Price is $" + str(price) + " Buy")
        print(output.format(price,"Buy"))
    else:
        print("Price is $" + str(price) + " Hold")
################################################################

#%% Exercise 4

grades = {'Bob':71, 'Alice':65, 'Jim':70, 'Jen':90, 'Tim':86, 'Trish':85, 'Tony':75}
letter_grades = {}

for key in grades.keys():
    value = grades[key]
    if value >= 90:
        letter_grades[key] = 'A+'
    elif grades[key] >= 85:
        letter_grades[key] = 'A'
    elif grades[key] >= 80:
        letter_grades[key] = 'A-'
    elif grades[key] >= 75:
        letter_grades[key] = 'B+'
    elif grades[key] >= 70:
        letter_grades[key] = 'B'
    elif grades[key] >= 65:
        letter_grades[key] = 'B-'
    else:
        letter_grades[key] = 'F'
print(letter_grades)
################################################################
#%% Exercise 5
mylist = ['A','B','C','D','D','D']

while 'D' in mylist:
    mylist.remove('D')

print(mylist)
################################################################

#%% Exercise 6
#Convert string $123,456,789 into a useable integer
deal_value = '$123,456,789'
deal_value = deal_value.strip('$')
deal_split = deal_value.split(',')
n = len(deal_split)
num_value = 0 # Initalize the variable because need to incrementally add
for i in range(n):
    calc = int(deal_split[i])
    num_value = num_value + calc * 1000**(n-1-i)
    print(calc * 1000**(n-1-i))

print(num_value)
################################################################

#%% Exercise 7
import numpy as np
def stockmove(stockdict):
    stockmoves = {}
    for key in stockdict.keys():
        price = stockdict[key]
        moves = []
        for i in range(5):
            price = price + np.random.randn()
            moves.append(price)
        stockmoves[key] = moves
    return(stockmoves)

np.random.seed(42) #set seed to compare results

stocks = {'AAPL':100.0, 'CAT':50.0, 'MSFT':150}

pricemoves = stockmove(stocks)

for key in pricemoves.keys():
    print(key + ": " + ', '.join("${:.2f}".format(i) for i in pricemoves[key]))
################################################################

#%% Exercise 8
#generate an array of simulated monthly returns (60 obs), with means 1-5 and std 1-5, 25 total assets
import numpy as np
np.set_printoptions(threshold=np.nan, precision=4, linewidth=150, suppress=True)
np.random.seed(42)
n = 60 #number of observations
m = 25 #number of assets

simrtns = np.zeros((n,m))

for i in range(5): #loop over means
    for j in range(5): #loop over std
        for k in range(0, simrtns.shape[0]): #loop over rows
            simrtns[k, 5*(i)+j] = np.random.normal(i+1,j+1)

#calculate covariance matrix and simulated means
mxmu = simrtns.mean(0) #array of all the asset means
print(mxmu)

mxsig = np.cov(simrtns, rowvar=False)
    #rowvar=True (default), assumes each row represents a variable, 
    #in this situation we want false, since each column is a different asset

mxsiginv = np.linalg.inv(mxsig) #inverse of a matrix

print(mxsig)
print(np.matmul(mxsig,mxsiginv))