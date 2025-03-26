import pandas as pd
import plotly.graph_objects as go
import os
import json
from pathlib import Path

# Load Configuration
config_path = Path("config/config.json")
if not config_path.exists():
    raise FileNotFoundError(f"Config file not found at {config_path}")

with open(config_path, 'r') as file:
    config = json.load(file)

# Extract values from config
short_window = config.get('short_window', 10)
long_window = config.get('long_window', 50)
data_path = "D:\\Coding\\ai_trading_bot\\ai_forex_trading_bot\\data\\gbpusd_data_OHLC_1H.parquet_56.parquet"
chart_width = config.get('chart_width', 1200)
chart_height = config.get('chart_height', 600)

# # Check if data exists
# if not data_path.exists():
#     raise FileNotFoundError(f"Data file not found at {data_path}")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

class SmaCrossoverStrategy:
    def __init__(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        # Calculate Simple Moving Averages (SMA)
        data['SMA_Short'] = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        data['SMA_Long'] = data['Close'].rolling(window=self.long_window, min_periods=1).mean()

        # Generate buy/sell signals
        data['Signal'] = 0
        data.loc[(data.index >= self.long_window) & (data['SMA_Short'] > data['SMA_Long']), 'Signal'] = 1
        data.loc[(data.index >= self.long_window) & (data['SMA_Short'] <= data['SMA_Long']), 'Signal'] = -1

        return data

# Load Data
df = pd.read_parquet(data_path)
df = df[~df['DateTime'].dt.weekday.isin([5, 6])]

# Check for missing values
print("Missing values per column: ")
print(df.isnull().sum())

# Apply SMA Strategy
strategy = SmaCrossoverStrategy(short_window, long_window)
df = strategy.generate_signals(df)

# Plot Candlestick Chart with SMAs
fig = go.Figure(data=[go.Candlestick(
    x=df['DateTime'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="GBP/USD"
)])

fig.add_trace(go.Scatter(x=df['DateTime'], y=df['SMA_Short'], mode='lines',
                         name=f'{short_window} SMA', line=dict(color='blue')))

fig.add_trace(go.Scatter(x=df['DateTime'], y=df['SMA_Long'], mode='lines',
                         name=f'{long_window} SMA', line=dict(color='red')))

fig.update_layout(
    title='GBP/USD Candlestick Chart with SMA Crossover',
    xaxis_title='DateTime',
    yaxis_title='Price',
    xaxis_rangeslider_visible=True,
    width=chart_width,
    height=chart_height,
    template="plotly_dark"
)

fig.show()

# Display Result Data
print(df[['DateTime', 'Close', 'SMA_Short', 'SMA_Long', 'Signal']].head())
