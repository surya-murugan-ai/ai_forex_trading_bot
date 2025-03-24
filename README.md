# AI Forex Trading Bot

## Overview
This project is an AI-powered Forex trading bot using a Simple Moving Average (SMA) Crossover strategy. It performs backtesting, evaluates the results, and visualizes the performance using Plotly.

## Project Structure
```
ai_forex_trading_bot/
├── data/                    # Store downloaded historical data
├── strategies/              # Contains the SMA crossover strategy
│   ├── sma_crossover.py
├── backtest.py              # Perform backtesting
├── evaluate.py              # Evaluate strategy performance
├── visualize.py             # Plot the results using Plotly
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/surya-murugan-ai/ai_forex_trading_bot.git
cd ai_forex_trading_bot
```
2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Place your historical data in the `data` folder.
2. Run the SMA crossover strategy:
```bash
python trading_bot.py
```
3. Perform backtesting:
```bash
python backtest.py
```
4. Evaluate the performance:
```bash
python evaluate.py
```
5. Visualize the results:
```bash
python visualize.py
```

## Strategy Explanation
- **SMA Crossover Strategy**: Uses two moving averages - a short-term SMA and a long-term SMA.
  - **Buy Signal**: When the short SMA crosses above the long SMA.
  - **Sell Signal**: When the short SMA crosses below the long SMA.

## Contributing
Feel free to fork this repository and contribute by submitting pull requests.

## License
This project is licensed under the MIT License.
