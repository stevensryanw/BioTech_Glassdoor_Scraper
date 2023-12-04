import yfinance as yf
import pandas as pd
import time

#Read in biotech.csv
symbols = pd.read_csv('symbols.csv')
#Just get column 1 with no index
symbols_noidx = symbols.iloc[:, 1]

#Lets just print the name of the first symbol via yfinance
# ticker = yf.Ticker(symbols_noidx[0])
# infod = ticker.info
# name = infod['shortName']
# print(name)



#Create a dataframe from comps
comps = []

for symbol in symbols_noidx:
    try:
        #Get the ticker data
        ticker = yf.Ticker(symbol)
        #Get the info
        infod = ticker.info
        #Get the company name and industry
        name = infod['shortName']
        industry = infod['industry']
        sector = infod['sector']
        #Append the name symbol and industry to comps
        comps.append([name, symbol, industry, sector])
        print(name, symbol, industry, sector)
        time.sleep(1)
    except:
        continue

df = pd.DataFrame(comps, columns=['name', 'symbol', 'industry', 'sector'])

#Save the dataframe to a csv
df.to_csv('biotech_comps.csv', index=False)

