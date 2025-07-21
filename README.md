# Hyperliquid Pump Chart Monitor

A comprehensive monitoring system that fetches pump chart data from Hyperliquid every 10 minutes and provides detailed technical analysis.

## Features

- 🔄 **Real-time Monitoring**: Fetches data every 10 minutes from Hyperliquid API
- 📊 **Technical Analysis**: Comprehensive TA including:
  - Moving Averages (SMA 9, 20, 50)
  - Exponential Moving Averages (EMA 12, 26)
  - RSI (Relative Strength Index)
  - Bollinger Bands
  - MACD (Moving Average Convergence Divergence)
  - Volume Analysis
  - Support & Resistance Levels
- 🚨 **Trading Signals**: Automated signal generation based on technical indicators
- 📈 **WebSocket Integration**: Real-time price updates
- 💾 **Data Persistence**: Saves analysis history to JSON files
- 🎯 **Multi-Token Support**: Monitor any token available on Hyperliquid

## Installation

1. **Clone or download the files**:
   ```bash
   # If you have git
   git clone <repository-url>
   cd hyperliquid-monitor
   
   # Or simply download the files to a directory
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Make the script executable** (Linux/Mac):
   ```bash
   chmod +x hyperliquid_monitor.py
   ```

## Usage

### Basic Usage

Monitor PUMP token (the target of your request):
```bash
python3 hyperliquid_simple_monitor.py --token PUMP
# OR use the convenient startup script:
./start_pump_monitor.sh
```

Monitor other tokens:
```bash
python3 hyperliquid_simple_monitor.py --token PURR
python3 hyperliquid_simple_monitor.py --token HYPE
```

### List Available Tokens

See all available tokens on Hyperliquid:
```bash
python3 hyperliquid_simple_monitor.py --list-tokens
```

### Command Line Options

- `--token TOKEN`: Specify the token symbol to monitor (default: PURR)
- `--list-tokens`: List all available tokens and exit
- `--help`: Show help message

## Output

The monitor provides:

1. **Console Output**: Real-time analysis reports every 10 minutes
2. **Log File**: `hyperliquid_monitor.log` with detailed logging
3. **JSON Data**: `hyperliquid_{TOKEN}_analysis.json` with historical analysis data

### Sample Output

```
================================================================================
HYPERLIQUID PURR TECHNICAL ANALYSIS REPORT
Time: 2024-01-15T10:30:00.123456
================================================================================

📊 CURRENT MARKET DATA:
Price: $0.142500
Volume (24h): $8,906.00
24h Change: 🟢 2.45%
Volume Change: 📈 15.30%

📈 TREND INDICATORS:
SMA_9: $0.141230
SMA_20: $0.139850
SMA_50: $0.138200
EMA_12: $0.141890
EMA_26: $0.140120

⚡ MOMENTUM INDICATORS:
RSI: 62.3400
MACD_Line: 0.0018
MACD_Signal: 0.0012
MACD_Histogram: 0.0006

🎯 VOLATILITY INDICATORS:
BB_Upper: $0.145600
BB_Middle: $0.142100
BB_Lower: $0.138600
BB_Width: 0.0493

🔄 SUPPORT & RESISTANCE:
Support: $0.138200
Resistance: $0.146800

🚨 TRADING SIGNALS:
• Price above SMA_9 - Bullish
• Price above SMA_20 - Bullish
• Price above SMA_50 - Bullish
• Golden Cross - Bullish EMA crossover
• RSI above 50 - Bullish momentum
• MACD bullish crossover
• High volume spike - Increased interest
================================================================================
```

## Technical Indicators Explained

### Moving Averages
- **SMA (Simple Moving Average)**: Average price over specific periods
- **EMA (Exponential Moving Average)**: Gives more weight to recent prices

### Momentum Indicators
- **RSI**: Measures overbought/oversold conditions (0-100)
  - Above 70: Potentially overbought
  - Below 30: Potentially oversold
- **MACD**: Shows relationship between two moving averages
  - Bullish when MACD line > Signal line
  - Bearish when MACD line < Signal line

### Volatility Indicators
- **Bollinger Bands**: Price channels based on standard deviation
  - Price touching upper band: Potentially overbought
  - Price touching lower band: Potentially oversold
  - Band squeeze: Low volatility, potential breakout

### Volume Analysis
- Compares current volume to recent average
- High volume often confirms price movements

## Monitoring Different Tokens

To monitor different tokens, first check what's available:

```bash
python3 hyperliquid_monitor.py --list-tokens
```

Then monitor your chosen token:

```bash
# For HYPE token
python3 hyperliquid_monitor.py --token HYPE

# For any other available token
python3 hyperliquid_monitor.py --token TOKEN_SYMBOL
```

## Data Files

### Log File (`hyperliquid_monitor.log`)
Contains detailed logging information including:
- API requests and responses
- WebSocket connection status
- Error messages and debugging info

### Analysis File (`hyperliquid_{TOKEN}_analysis.json`)
JSON file containing:
- Historical analysis data (last 100 analyses)
- All technical indicators
- Trading signals
- Market data snapshots

## Stopping the Monitor

- **Ctrl+C**: Gracefully stops the monitor
- The system will close WebSocket connections and save any pending data

## Requirements

- Python 3.7+
- Internet connection
- The following Python packages (installed via requirements.txt):
  - requests
  - websocket-client
  - pandas
  - numpy

## API Information

This monitor uses the Hyperliquid public API:
- **API Base URL**: https://api.hyperliquid.xyz
- **WebSocket URL**: wss://api.hyperliquid.xyz/ws
- **Rate Limits**: Respects Hyperliquid's rate limiting
- **No API Key Required**: Uses public endpoints only

## Troubleshooting

### Common Issues

1. **"Token not found" error**:
   - Check available tokens with `--list-tokens`
   - Ensure token symbol is spelled correctly
   - Some tokens might not have spot trading enabled

2. **WebSocket connection issues**:
   - Check internet connection
   - Hyperliquid servers might be temporarily unavailable
   - The monitor will continue with REST API only

3. **"Insufficient data for analysis"**:
   - Normal for the first few minutes
   - Technical indicators need historical data to calculate

4. **Permission denied (Linux/Mac)**:
   ```bash
   chmod +x hyperliquid_monitor.py
   ```

### Getting Help

- Check the log file for detailed error messages
- Ensure all dependencies are installed correctly
- Verify internet connection and API availability

## Disclaimer

This tool is for educational and informational purposes only. It is not financial advice. Always do your own research before making trading decisions. Cryptocurrency trading involves significant risk.

## Contributing

Feel free to submit issues, feature requests, or improvements to enhance the monitoring system.