#Please run the following code on QuantConnect

#Don't naviely run the strategy and believe this can make money. No one will share the robust and profitable strategy. No one

import pandas as pd
from datetime import datetime

class SectorMomentumAlgorithm(QCAlgorithm):

    def Initialize(self):

        self.SetStartDate(2005, 1, 1)  
        self.SetEndDate(datetime.now())  
        self.SetCash(100000) 
        # create a dictionary to store momentum indicators for all symbols 
        self.data = {}
        period = 252
        # choose ten sector ETFs
        self.symbols = ["XLB",  # Materials Select Sector SPDR Fund
                        "XLV",  # Health Care Select Sector SPDR Fund
                        "XLC",  # Communication Services Select Sector SPDR Fund
                        "XLK",  # Technology Select Sector SPDR Fund
                        "XLF",  # Financial Select Sector SPDR Fund
                        "XLP",  # Consumer Staples Select Sector SPDR Fund
                        "XLI",  # Industrial Select Sector SPDR Fund
                        "XLU",  # Utilities Select Sector SPDR Fund
                        "XLY",  # Consumer Discretionary Select Sector SPDR Fund
                        "XLE",  # Energy Select Sector SPDR Fund
                        "XLRE"]  # Real Estate Select Sector SPDR Fund
                        
        # warm up the MOM indicator
        self.SetWarmUp(period)
        for symbol in self.symbols:
            self.AddEquity(symbol, Resolution.Daily)
            self.data[symbol] = self.ROC(symbol, period, Resolution.Daily)
        # shcedule the function to fire at the month start 
        self.Schedule.On(self.DateRules.MonthStart("XLK"), self.TimeRules.AfterMarketOpen("XLK"), self.Rebalance)
            
    def OnData(self, data):
        pass

    def Rebalance(self):
        if self.IsWarmingUp: return
        top3 = pd.Series(self.data).sort_values(ascending = False)[:1]
        for kvp in self.Portfolio:
            security_hold = kvp.Value
            # liquidate the security which is no longer in the top3 momentum list
            if security_hold.Invested and (security_hold.Symbol.Value not in top3.index):
                self.Liquidate(security_hold.Symbol)
        
        for symbol in top3.index:
            self.SetHoldings(symbol, 1/len(top3))
