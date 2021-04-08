import yfinance as yf
from core.database import Database
import pandas as pd

class LiquidityCalc:
    def __init__(self):
        pass
    @staticmethod
    def getStocks(df):
        isins = df['ISIN'].values
        return isins
    @staticmethod
    def readText():
        f = open('./core/stocks.txt', 'r')
        lines = f.readlines()
        stocks = []
        for line in lines:
            stocks.append(line.strip())
        return stocks
    @staticmethod
    def getNames(isins):
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
        comp = []
        isin = []
        tenDayAvgVol = []
        tenDayAvg = []
        stock_price = []
        market_cap = []
        for k, stoc in zip(isins.keys(), stocks):
            stock = isins[k] + str('.NS')
            data = yf.Ticker(stock).info
            comp.append(data['shortName'])
            price = yf.download(tickers=stock, period='1d')['Adj Close'].values[0]
            stock_price.append(price)
            isin.append(k)
            tenDayAvg.append(price*data['averageVolume10days']/10000000)
            tenDayAvgVol.append(data['averageVolume10days'])
            market_cap.append(data['marketCap']/10000000)


        df = pd.DataFrame({'Company': comp, 'isin': isin, '10 D ADV': tenDayAvgVol, 'Price': stock_price, 'Market Cap ( In Cr)': market_cap, '10 D Average Volume (In Cr)': tenDayAvg})
        print(df)
        return df
