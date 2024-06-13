# Pandas Fundamentals + Groupby Example

# Say we need to merge stock price/return data with financials (B/M is a common control variable)

financials = pd.read_csv('../StockData/fundamentals.csv', index_col=0)
aapl = pd.read_csv('../StockData/AAPL.csv', header=0)
# Convert to date time type (provides functions to easier move dates around)
aapl['Date'] = pd.to_datetime(aapl['Date'])
# Convert to month end to handle alignment with reporting date
aapl['Match Date'] = aapl['Date'] + pd.offsets.MonthEnd(-1) # using the previous month end to not have information to early
print(aapl.head(30))

# Check for Apple data, notice that it is all for year ending
# On top of that, the information isn't truly known until it is disclosed. Common practice is to carry the previous years
# data. For 2015 use 2014
print(financials[financials['Ticker Symbol']=='AAPL'].head())
print(financials.info())

# Convert to date time
financials['Period Ending'] = pd.to_datetime(financials['Period Ending'])
# Create the same match dimension
financials['Match Date'] = financials['Period Ending'] + pd.offsets.MonthEnd(0)
print(financials[financials['Ticker Symbol']=='AAPL'].head())

# filter for only apple financials, and the required columns to calculate B/M, don't forget the match dimension
aapl_financials = financials[financials['Ticker Symbol']=='AAPL'][['Total Equity','Estimated Shares Outstanding','Match Date']]
print(aapl_financials)

# Find the max and min so we can truncate the merge set
max_date = max(aapl_financials['Match Date'])
min_date = min(aapl_financials['Match Date'])

# Need to merge with how='left' so we keep all values on the left for the inbetween days, otherwise it will just result in 4 matches
# on the exact values
aapl = aapl.merge(aapl_financials, how='left', left_on='Match Date', right_on='Match Date')

# apply the forward fill, because we fill to the date when the value would first apply (for 2017, using FY2016 data)
# then push foward to fill the values
aapl[['Total Equity', 'Estimated Shares Outstanding', 'Match Date']] = aapl[['Total Equity', 'Estimated Shares Outstanding', 'Match Date']].fillna(method='ffill') 
print(aapl.info())
#drop the blanks
aapl = aapl.dropna()
print(aapl.head())
print(aapl.tail()) #Notice that we fill to far forward, we can use the max to remove the ones that are out of sample

# keep only the values that are less then the maximum date in the dataframe
# need to convert types so we can add the offset, and then convert back to period datatype
aapl = aapl[aapl['Match Date'] <= (max_date + pd.DateOffset(years=1))]
print(aapl.tail())

# Remove the match column, not required anymore
print(aapl.head())
aapl.drop(labels='Match Date',axis=1, inplace=True)
print(aapl.head())

# Calculate the B/M value
aapl['BM'] = aapl['Total Equity']/(aapl['Adj Close'] * aapl['Estimated Shares Outstanding'])
aapl.head()

# Using the merge function, we don't need to create the subset dataframe if we have an additional dimension
# Loading the data again
financials = pd.read_csv('../StockData/fundamentals.csv', index_col=0)
aapl = pd.read_csv('../StockData/AAPL.csv', header=0, parse_dates = True)
# Convert to date time type (provides functions to easier move dates around)
aapl['Date'] = pd.to_datetime(aapl['Date'])
# Convert to month end to handle alignment with reporting date
aapl['Match Date'] = aapl['Date'] + pd.offsets.MonthEnd(-1) # using the previous month end to not have information to early
# Creating a ticker variable, it is common to have a variable for the asset when dealing with portfolios
aapl['Ticker'] = 'AAPL'
print(aapl.head(30))

financials['Period Ending'] = pd.to_datetime(financials['Period Ending'])
# Create the same match dimension
financials['Match Date'] = financials['Period Ending'] + pd.offsets.MonthEnd(0)

# Need to merge with how='left' so we keep all values on the left for the inbetween days, otherwise it will just result in 4 match months
# on the exact values
aapl = aapl.merge(financials[['Ticker Symbol','Total Equity', 'Estimated Shares Outstanding', 'Match Date']], how='left', left_on=['Match Date','Ticker'], right_on=['Match Date','Ticker Symbol'])
aapl.info()
# Notice how the Match Date column was not duplicated, but the Ticker Column was. This is because of the names not being exact

max_date = max(financials[financials['Ticker Symbol'] == 'AAPL']['Match Date'])
aapl = aapl[aapl['Match Date'] <= (max_date + pd.DateOffset(years=1))]

# apply the forward fill, because we fill to the date when the value would first apply (for 2017, using FY2016 data)
# then push foward to fill the values
aapl[['Total Equity', 'Estimated Shares Outstanding', 'Match Date']] = aapl[['Total Equity', 'Estimated Shares Outstanding', 'Match Date']].fillna(method='ffill') 

print(aapl.tail())

# Notice how we still have an NaN in the column for Ticker Symbol, if we were to run dropna() now it will clear out all rows that have the missing observation
# This is typical behaviour when processing data because you typically want full obersvations when performing analysis

aapl.drop(labels=['Match Date', 'Ticker Symbol'],axis=1, inplace=True)
print(aapl.head())
####################################################################################################
# Viz Data Mean/Std/Volume Function
def mean_sig_vol(data):
    mu = data['logrtn'].mean()*100
    sig = data['logrtn'].std()*100
    totvol = data['Volume'].sum()
    df = {'mu':[mu],
          'sigma':[sig],
          'totalvol':[totvol]}
    df = pd.DataFrame(data=df)
    return df

####################################################################################################
# Analysis Bootstrap function
def bootcoef(X, y, nboot=999):
    #Range of sample index, this allows for pairs sampling
    inds = np.arange(len(X))
    temp_reg = sm.OLS(y, X).fit()
    bootresults = temp_reg.params.tolist()
    for i in range(nboot):
        # generate a random set of integers to select a bootstrap sample from data
        bootint = np.random.choice(inds, len(inds))
        Xboot = X[bootint]
        yboot = y[bootint]
        temp_reg = sm.OLS(yboot, Xboot).fit()
        bootresults.extend(temp_reg.params.tolist())
    return(bootresults)