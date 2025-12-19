import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd
import os
import smtplib
import ssl
from dotenv import load_dotenv

load_dotenv()
stocks = [
    ("Apple", "AAPL"),
    ("Microsoft", "MSFT"),
    ("Nvidia", "NVDA"),
    ("Amazon", "AMZN"),
    ("Alphabet", "GOOGL"),
    ("Meta", "META"),
    ("Tesla", "TSLA"),
    ("Walmart", "WMT"),
    ("JPMorgan Chase", "JPM"),
    ("Visa", "V"),
    ("Mastercard", "MA"),
    ("Netflix", "NFLX"),
    ("Bank of America", "BAC"),
    ("Oracle", "ORCL"),
    ("Coca-Cola", "KO")
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_stock_price(ticker):
    """Fetch current stock price from Yahoo Finance"""
    try:
        url = f'https://finance.yahoo.com/quote/{ticker}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        price_element = soup.find('span', {'data-testid': 'qsp-price'})
        if price_element:
            price = float(price_element.text.replace(',', ''))
            return price
        return None
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def send_mail(message):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as smtp:
        smtp.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
        smtp.sendmail(os.getenv("EMAIL"), os.getenv("EMAIL"), message)
    print("Alert Email Sent!")

if os.path.exists('stocks.csv'):
    df = pd.read_csv("stocks.csv")

    for stock in df.to_dict("records"):
        ticker = (stock["Ticker"])
        stock_price = get_stock_price(ticker)

        if stock_price is None:
            print(f"Failed to fetch price for {ticker}")
            continue

        time.sleep(1.5)

        if stock_price <= stock["Alert Price Low"]:
            subject = "Stock Price Alert!"
            body = f"{stock['Company']} dropped below your alert price {stock['Alert Price Low']}"
            email = f"Subject:{subject}\n\n{body}"
            send_mail(email)

        elif stock_price >= stock["Alert Price High"]:
            subject = "Stock Price Alert!"
            body = f"{stock['Company']} went above your alert price {stock['Alert Price High']}"
            email = f"Subject:{subject}\n\n{body}"
            send_mail(email)

if os.path.exists('stocks.csv') == False:
    with open('stocks.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Company', 'Ticker', 'Current Price', 'Alert Price Low', 'Alert Price High'])
        
        for i, (company, ticker) in enumerate(stocks, 1):
            print(f"Fetching {i}/15: {company} ({ticker})...")
            
            price = get_stock_price(ticker)
            
            if price:
                alert_low = round(price * 0.90, 2)
                alert_high = round(price * 1.10, 2)
                
                writer.writerow([company, ticker, price, alert_low, alert_high])
                print(f"  ✓ {company}: ${price:.2f}")
            else:
                writer.writerow([company, ticker, "N/A", "N/A", "N/A"])
                print(f"  ✗ Failed to fetch {company}")
            
            if i < len(stocks):
                time.sleep(1.5)

    print("\n✓ CSV file 'stocks.csv' created successfully!")
