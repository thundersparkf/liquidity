import yfinance as yf
from core.database import Database
import pandas as pd

class LiquidityCalc:
    def __init__(self):
        pass
    def getStocks(self, df):
        isins = df['ISIN'].values
        return isins
    def readText(self):
        f = open('./core/stocks.txt', 'r')
        lines = f.readlines()
        stocks = []
        for line in lines:
            stocks.append(line.strip())
        return stocks
    def getNames(self, isins):
        db = Database()
        sql = """SELECT * FROM nse_isins WHERE isin_code =ANY (%s)"""
        results = db.pullData(sql, isins)
        dict = {}
        for result in results:
            dict[result[0]] = result[1]
        return dict
    def getVol(self):
        stocks = self.readText()
        isins = self.getNames(stocks)
        isin = []
        tenDayAvgVol = []
        tenDayAvg = []
        stock_price = []
        market_cap = []
        for k in isins.keys():
            stock = isins[k] + str('.NS')
            data = yf.Ticker(stock).info
            price = yf.download(tickers=stock, period='1d')['Adj Close'].values[0]
            stock_price.append(price)
            isin.append(k)
            tenDayAvg.append(price*data['averageVolume10days'])
            tenDayAvgVol.append(data['averageVolume10days'])
            market_cap.append(data['marketCap'])


        df = pd.DataFrame({'isin': isin, '10DayAvgTradingVol': tenDayAvgVol, 'stock_price': stock_price, 'market_cap': market_cap, '10DayAvgVol': tenDayAvg})
        print(df)
        return df
