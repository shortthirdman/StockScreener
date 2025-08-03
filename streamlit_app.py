import sys

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

import os
import math
import random
import requests

from datetime import datetime
from pytickersymbols import PyTickerSymbols

# stock_data = PyTickerSymbols()
# countries = stock_data.get_all_countries()
# indices = stock_data.get_all_indices()
# industries = stock_data.get_all_industries()

st.set_page_config(
    page_title="Stock Screener",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state=None,
    menu_items={
        'Get Help': 'https://www.github.com/shortthirdman/StockScreener/',
        'Report a bug': "https://www.github.com/shortthirdman/StockScreener/issues",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.title("🎈 Stock Screener")
st.write("Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/).")

st.write("This app is a simple stock screener that evaluates stocks based on their performance against a benchmark index (S&P 500 by default). It calculates various financial ratios and provides insights into the risk and return characteristics of the selected stocks.")
st.markdown("""
### Features:
- Fetches historical stock data using Yahoo Finance.
- Calculates financial ratios: Beta, Sharpe Ratio, Sortino Ratio, Alpha, and Treynor Ratio.
- Provides human-readable remarks based on the calculated ratios.
- Allows filtering of stocks based on specific criteria.
### Usage:
1. Click the "Build Screener" button to generate the stock screener.
2. The screener will display a table with the calculated financial ratios for each stock.
3. You can modify the list of tickers in the code to analyze different stocks.
""")
st.write("### Financial Ratios:")
st.write("- **Beta** shows sensitivity to the market")
st.write("- **Sharpe Ratio** measures return per unit of total risk")
st.write("- **Sortino Ratio** measures return per unit of downside risk only — a more realistic view")

def ensure_list(data):
    """
    Checks if the input data is a list. If not, attempts to convert it to a list.
    Handles non-iterable inputs by wrapping them in a list.
    """
    if not isinstance(data, list):
        try:
            # Attempt to convert iterable data to a list
            data = list(data)
        except TypeError:
            # If not iterable, wrap the single item in a list
            data = [data]
    return data

def fetch_data(tickers, index='^GSPC', period='1y', interval='1d'):
    all_tickers = tickers + [index]
    df = yf.download(all_tickers, period=period, interval=interval)['Close']
    return df

def calculate_ratios(returns, benchmark_returns, risk_free_rate=0.04/252):
    excess = returns - risk_free_rate
    downside = excess[excess < 0]

    beta = np.cov(returns, benchmark_returns)[0,1] / np.var(benchmark_returns)
    sharpe = np.mean(excess) / np.std(returns)
    sortino = np.mean(excess) / np.std(downside) if len(downside) > 0 else np.nan
    
    avg_return = np.mean(returns)
    avg_benchmark = np.mean(benchmark_returns)
    
    # CAPM expected return
    expected_return = risk_free_rate + beta * (avg_benchmark - risk_free_rate)

    # Annualized alpha
    alpha = (avg_return - expected_return) * 252

    # Treynor ratio (annualized excess return over beta)
    treynor = ((avg_return - risk_free_rate) * 252) / beta if beta != 0 else np.nan

    return beta, sharpe, sortino, alpha, treynor


def build_screener(tickers, index='^GSPC', period='1y', risk_free_rate=0.04/252, filter=False):
    df = fetch_data(tickers, index=index, period=period)
    benchmark = df[index].pct_change().dropna()
    results = []
    
    for ticker in tickers:
        ret = df[ticker].pct_change().dropna()
        aligned = pd.concat([ret, benchmark], axis=1, join='inner').dropna()
        beta, sharpe, sortino, alpha, treynor = calculate_ratios(aligned[ticker], aligned[index], risk_free_rate)

        # Generate human-readable remark
        if beta < 0.8:
            beta_remark = "Defensive or low volatility"
        elif beta <= 1.2:
            beta_remark = "Market-neutral behavior"
        else:
            beta_remark = "High volatility / aggressive"

        if sharpe < 1.0:
            sharpe_remark = "Suboptimal risk-adjusted return"
        elif sharpe < 2.0:
            sharpe_remark = "Acceptable performance"
        else:
            sharpe_remark = "Excellent risk-adjusted return"

        remark = f"{beta_remark}; {sharpe_remark}"

        results.append({
            'Ticker': ticker,
            'Beta': beta,
            'Sharpe Ratio': sharpe,
            'Sortino Ratio': sortino,
            'Alpha': alpha,
            'Treynor Ratio': treynor,
            'Remark': remark
        })

    df = pd.DataFrame(results).sort_values('Sharpe Ratio', ascending=False)
    if filter is True:
        filtered = df[(df['Beta'] < 1) & (df['Sharpe Ratio'] > 1.2)]
        return filtered.reset_index(drop=True)[['Ticker', 'Beta', 'Sharpe Ratio', 'Sortino Ratio', 'Alpha', 'Treynor Ratio', 'Remark']]
    else:
        return df.reset_index(drop=True)[['Ticker', 'Beta', 'Sharpe Ratio', 'Sortino Ratio', 'Alpha', 'Treynor Ratio', 'Remark']]

if st.button("Build Screener"):
    tickers = ['AAPL','MSFT','GOOGL','TSLA','KO','NVDA']
    df = build_screener(tickers, index='^GSPC', period='1y')
    st.table(df)

col1, col2, col3 = st.columns(3)
