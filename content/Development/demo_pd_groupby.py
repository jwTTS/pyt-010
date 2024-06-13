import pandas as pd

holdings = pd.read_csv('ExData/Holdings.csv', parse_dates=[0])

# make columns lowercase, easier to type
holdings.columns = [i.lower() for i in holdings.columns]

holdings.info()
holdings.head()
holdings.tail()

print(holdings.groupby('ticker'))
print(holdings.groupby('ticker').head(2))

holdings.groupby('ticker').head(1)

for name, group in holdings.groupby('ticker'):
    print(name)
    print(group)

# Notice how shift doesn't work correctly, it ignores the ticker symbol
holdings['shares_1'] = holdings['shares'].shift(1)
holdings.head()

# Using groupby lets python know how the data is related 
holdings['shares_1'] = holdings.groupby('ticker')['shares'].shift(1)
holdings.head()

# Calculate the change in shares
holdings['dshares'] = holdings['shares'] - holdings['shares_1']

holdings.head()
holdings.tail()

# We can automate the loading of our stock data using the ticker symbols and a loop
tickers = holdings['ticker'].drop_duplicates().values.tolist()

tempdf = []
for ticker in tickers:
    inputfile = 'StockData/%s.csv' % ticker
    tempdata = pd.read_csv(inputfile, header=0)
    tempdata['ticker'] = ticker
    tempdf.append(tempdata) # This makes a copy of the dataframe into the list, remember the example like when assigning values using variables.

stockdata = pd.concat(tempdf)

stockdata.groupby('ticker').head(2)
stockdata.columns = [i.lower().replace(' ','_') for i in stockdata.columns]

stockdata['date'] = pd.to_datetime(stockdata['date'], format=r'%Y-%m-%d')
stockdata.set_index('date', inplace=True)

# By only specifying one column in the aggregation method we are only processing that one variable
stockprice = stockdata.groupby(['ticker']).resample('Q').agg({'adj_close':'last'})

stockprice.reset_index(inplace=True)
stockprice.groupby('ticker').head(2)

portfolio = holdings.merge(stockprice, how='left') # column names are identical so I don't need to specify anything

# Check our work, notice that the correct prices were carried over
portfolio.head()
stockprice[stockprice['date'] == '2017-03-31']

# Now we can calculate our position/holding values 
portfolio['hvalue'] = portfolio['shares'] * portfolio['adj_close']
portfolio.head()

# Now let's try to calculate the total portfolio value for each quarter
portfolio.groupby('date')['hvalue'].sum()

# Assign the value to the original dataframe
portfolio['tvalue'] = portfolio.groupby('date')['hvalue'].sum()
portfolio # all NAs

# Remove the column from the dataframe
portfolio.drop('tvalue', axis=1, inplace=True)

# Create a temp dataframe to store the totals per quarter
tvalue = portfolio.groupby('date')['hvalue'].sum()

# Merge the totals with the original
tvalue = pd.DataFrame(tvalue) # When it is a single column, typically a series will be created instead of a dataframe, if using v0.24+ can merge dataframes if they are named (df.rename(str))
tvalue.columns = ['tvalue'] #change the name of the column so it is not duplicated
tvalue.reset_index(inplace=True)
tvalue.info()
portfolio = portfolio.merge(tvalue, how='left', left_on='date', right_on='date')

portfolio

portfolio['w'] = portfolio['hvalue'] / portfolio['tvalue']

# Check sums to 1
portfolio.groupby('date')['w'].sum()