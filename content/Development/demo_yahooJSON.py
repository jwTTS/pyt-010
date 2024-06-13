"""
Program creates a quick comps table using live data from Yahoo Finance

"""
#%% Import Packages
import pandas as pd

#%% JSON for Yahoo Finance
#function that grabs a Yahoo Finance JSON URL and outputs the results as a DataFrame table
def fnYFinJSON(stock):
	urlData = "https://query2.finance.yahoo.com/v6/finance/quote?symbols="+stock
	df = pd.read_json(urlData)
	df = pd.DataFrame(df.iloc[1][0])#need to go down to result layer
	df.set_index('symbol', inplace=True) #renaming row as the ticker to keep track of data
	return df

#%% Create a comps table based on tickers and fields needed
tickers = ['AAPL', 'MSFT', 'TSLA', 'BA', 'META', 'AMZN', 'NFLX']
fields = {'shortName':'Company', 'bookValue':'Book Value', 'currency':'Curr',
		  'fiftyTwoWeekLow':'52W L', 'fiftyTwoWeekHigh':'52W H',
		  'regularMarketPrice':'Price', 'regularMarketDayHigh':'High', 
		  'regularMarketDayLow':'Low', 'priceToBook':'P/B', 'trailingPE':'LTM P/E'}

#joining all the ticker data
outputs = pd.DataFrame()
for ticker in tickers:
	currentTicker = fnYFinJSON(ticker)	
	outputs = pd.concat([outputs,currentTicker], axis=0, sort=False)

#renaming and pulling out only needed columns
outputs.rename(columns=fields, inplace=True)
filteredCols = list(fields.values())
filteredData = outputs[filteredCols]

#%% Output to Excel
filteredData.to_excel("OutputYFin.xlsx")