#%% Demo creating returns files for each ticker
import os
import pandas as pd

files = []
for file in os.listdir("StockData/"):
    if file.endswith(".csv"):
        files.append(file)

rules = {'Open':'first', 'Close':'last', 'High':'max', 'Low':'min','Volume':'sum'}


for fileName in files:
    ticker = fileName.replace(".csv","")
    df = pd.read_csv("StockData/" + file, parse_dates=['Date'], index_col=['Date'])
    df['Ticker'] = ticker
    df['Returns'] = df['Close'].pct_change()
    
    #Challenge
    df_mo = df.resample("M").agg(rules)
    df_mo['Returns'] = df_mo['Close'].pct_change()
    
    folderPath = "tickers/" + ticker
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
        df.to_csv(folderPath + "/" + ticker + "_returns.csv")
        df_mo.to_csv(folderPath + "/" + ticker + "_monthly.csv")