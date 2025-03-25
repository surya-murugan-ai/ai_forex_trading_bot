import pandas as pd
import plotly.graph_objects as go

#display all the rows without truncation
pd.set_option('display.max_rows',None)
pd.set_option('display.max_columns',None)

class SmaCrossoverStrategy:
    def __init__(self, short_window=10, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        # Calculate Simple Moving Averages (SMA)
        data['SMA_Short'] = data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        data['SMA_Long'] = data['Close'].rolling(window=self.long_window, min_periods=1).mean()

        # Generate buy/sell signals
        data['Signal'] = 0
        data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1
        data.loc[data['SMA_Short'] <= data['SMA_Long'], 'Signal'] = -1
        
        return data

# Load the data
df = pd.read_parquet('/home/sapat/learning ML/ai_forex_trading_bot/data/gbpusd_data_OHLC_1H.parquet_56.parquet')

# Remove weekends (No trading on Saturdays and Sundays)
df = df[~df['DateTime'].dt.weekday.isin([5, 6])]

# Verify missing data
print("Missing values per column: ")
print(df.isnull().sum())
# print(df.tail(100))

# Apply SMA strategy
strategy = SmaCrossoverStrategy()
df = strategy.generate_signals(df)

# Visualize data with SMA

#line graph
# fig = px.line(df, x='DateTime', y=['Close', 'SMA_Short', 'SMA_Long'], 
#                title='GBP/USD Closing Price with SMA Crossover')

# Plot Candlestick Chart with SMAs
fig = go.Figure(data=[go.Candlestick(
    x=df['DateTime'],
    open=df['Open'],
    high=df['High'],
    low=df['Low'],
    close=df['Close'],
    name="GBP/USD"
)])

# Plot Short-term SMA
fig.add_trace(go.Scatter(x=df['DateTime'],y=df['SMA_Short'],mode='lines',
                         name='10 SMA',line=dict(color='blue')))

fig.add_trace(go.Scatter(x=df['DateTime'],y=df['SMA_Long'],mode='lines',
                         name='50 SMA', line=dict(color='red')))

fig.update_layout(
    title='GBP/USD Candlestick Charts',
    xaxis_title='DataTIme',
    yaxis_title='Price',
    xaxis_rangeslider_visible=True,
    xaxis_rangeslider_thickness=0.1,
    template="plotly_dark",
    dragmode="zoom", #enable zooming
    hovermode = "x", #display hover information
    width=1200,  # Set width (in pixels)
    height=600, 
    margin = dict(l=50,r=50,t=50,b=50)

)

fig.show()

# Optional: Display a sample of the data
# print(df[['DateTime']].head())
print(df[['DateTime', 'Close', 'SMA_Short', 'SMA_Long', 'Signal']].head())
