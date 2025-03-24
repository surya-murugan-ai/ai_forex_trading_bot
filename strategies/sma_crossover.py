import pandas as pd


class SmaCrossoverStrategy:
    def __init__(self,short_window=10,long_window=50):
        self.short_window= short_window
        self.long_window = long_window
    
    def generate_signals(self, data):
        data['SMA_Short'] = data['Close'].rolling(window=self.short_window).mean()
        data['SMA_Long'] = data['Close'].rolling(window=self.long_window).mean()
        data['Signal'] = 0
        data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1
        data.loc[data['SMA_Short'] <= data['SMA_Long'], 'Signal'] = -1
        return data
        