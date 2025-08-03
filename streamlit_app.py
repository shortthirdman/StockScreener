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

st.title("🎈 Stock Screener")
st.write("Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/).")

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


def build_screener(tickers, index='^GSPC', period='1y', risk_free_rate=0.04/252):
    df = fetch_data(tickers, index=index, period=period)
    benchmark = df[index].pct_change().dropna()
    results = []
    
    for ticker in tickers:
        ret = df[ticker].pct_change().dropna()
        aligned = pd.concat([ret, benchmark], axis=1, join='inner').dropna()
        beta, sharpe, sortino, alpha, treynor = calculate_ratios(aligned[ticker], aligned[index], risk_free_rate)
        results.append({'Ticker': ticker, 'Beta': beta, 'Sharpe Ratio': sharpe, 'Sortino Ratio': sortino, 'Alpha': alpha, 'Treynor Ratio': treynor})
    
    return pd.DataFrame(results).sort_values('Sharpe Ratio', ascending=False).set_index('Ticker')

global df
if st.button("Build Screener"):
    tickers = ['AAPL','MSFT','GOOGL','TSLA','KO','NVDA']
    df = build_screener(tickers, index='^GSPC', period='1y')
    df.set_index('Ticker')
    st.table(df)

if st.button("Tune Screener"):
    filtered = df[(df['Beta'] < 1) & (df['Sharpe Ratio'] > 1.2)]
    st.write(filtered)


col1, col2, col3 = st.columns(3)
