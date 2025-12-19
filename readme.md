# Stock Price Alert System

A Python script that monitors stock prices from Yahoo Finance and sends email alerts when prices cross your defined thresholds.

## Features

- Scrapes real-time stock prices from Yahoo Finance
- Monitors 15 major stocks (customizable)
- Sends email alerts when stocks hit low or high alert prices
- Automatically creates CSV file with stock data on first run
- Sets alert thresholds at ±10% from current price

## Requirements

```bash
pip install requests beautifulsoup4 pandas python-dotenv
```

## Setup

1. **Clone or download this repository**

2. **Create a `.env` file** in the same directory with your email credentials:

```env
EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

> **Note:** For Gmail, you need to use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password. Enable 2FA first, then generate an app password.

3. **Run the script:**

```bash
python stock_alert.py
```

## How It Works

### First Run
- Creates `stocks.csv` with current prices for 15 stocks
- Sets alert thresholds at -10% (low) and +10% (high) from current price

### Subsequent Runs
- Reads `stocks.csv` and checks current prices
- Sends email alert if any stock crosses its threshold
- Waits 1.5 seconds between requests to respect Yahoo Finance

## Customization

### Add/Remove Stocks
Edit the `stocks` list in the script:

```python
stocks = [
    ("Apple", "AAPL"),
    ("Microsoft", "MSFT"),
    # Add more here...
]
```

### Change Alert Thresholds
Modify the percentage in the script (default is ±10%):

```python
alert_low = round(price * 0.90, 2)   # Change 0.90 for different %
alert_high = round(price * 1.10, 2)  # Change 1.10 for different %
```

Or manually edit the CSV file after it's created.

## Automation

### Run on a Schedule

**Linux/Mac (cron):**
```bash
# Run every hour
0 * * * * /usr/bin/python3 /path/to/stock_alert.py
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., hourly)
4. Action: Start a program → `python.exe`
5. Add arguments: `path\to\stock_alert.py`

## File Structure

```
.
├── stock_alert.py      # Main script
├── stocks.csv          # Generated stock data (auto-created)
├── .env               # Email credentials (you create this)
└── README.md          # This file
```

## Monitored Stocks (Default)

1. Apple (AAPL)
2. Microsoft (MSFT)
3. Nvidia (NVDA)
4. Amazon (AMZN)
5. Alphabet (GOOGL)
6. Meta (META)
7. Tesla (TSLA)
8. Walmart (WMT)
9. JPMorgan Chase (JPM)
10. Visa (V)
11. Mastercard (MA)
12. Netflix (NFLX)
13. Bank of America (BAC)
14. Oracle (ORCL)
15. Coca-Cola (KO)

## Troubleshooting

**No emails received?**
- Check your `.env` file has correct credentials
- For Gmail, make sure you're using an App Password
- Check spam folder

**"Failed to fetch price"?**
- Yahoo Finance may be blocking requests (too many too fast)
- Check your internet connection
- Try increasing the `time.sleep()` value

**CSV not updating?**
- Delete `stocks.csv` to regenerate with fresh data
- The script only creates CSV if it doesn't exist

## License

Free to use and modify as needed.

## Disclaimer

This tool is for educational purposes. Always verify stock information from official sources before making investment decisions.