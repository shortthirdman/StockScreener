# Stock Screener

Free Stock Screener in Python with Beta, Sharpe, and Sortino Ratios

---

#### Development Setup

- Create a Python virtual environment and activate

	```shell
	$ python -m venv --upgrade-deps --clear dev
	$ export PIP_CONFIG_FILE="pip.conf"
	```
	
	```pwsh
	$ ./dev/Scripts/activate
	```
	
	```bash
	$ source dev/bin/activate
	```

- Install the packages and dependencies as listed in requirements file

	```shell
	$ pip install -U -r requirements.txt --no-cache-dir --disable-pip-version-check
	```

- Start your local development StreamLit server

	```shell
	$ streamlit run streamlit_app.py
	```

---

#### What's Next

- Automate daily snapshots using cron jobs, Windows Task Scheduler, or hosted notebooks like Deepnote

- Send alerts via email, Telegram, or Slack when a stock's beta spikes or drops suddenly

- Store beta data in a SQL or time-series database like SQLite or InfluxDB for long-term analysis

- Visualize beta trends using Streamlit or Dash for interactive dashboards

- Add more filters from the FMP screener like price, sector, volume, or market cap

- Correlate beta changes with price movements to explore new signal-generation strategies

- Expand to weekly/monthly beta deltas to smooth out daily noise and highlight macro shifts

---

#### References

- [Track Stock Volatility Changes Daily](https://medium.com/@trading.dude/what-if-you-could-track-stock-volatility-changes-daily-build-this-screener-in-python-abeafd1753f5)

- [Build a Free Stock Screener in Python with Beta, Sharpe, and Sortino Ratios](https://python.plainenglish.io/build-a-free-stock-screener-in-python-with-beta-sharpe-and-sortino-ratios-139eeb1a909b)

- [Automate Alerts with Deepnote and Telegram in Python](https://python.plainenglish.io/automate-alerts-with-deepnote-and-telegram-in-python-a-step-by-step-guide-1214bd9dd03d)

- [The Ultimate Guide to Risk-Return Metrics for Stock Investors](https://medium.com/@trading.dude/the-ultimate-guide-to-risk-return-metrics-for-stock-investors-with-python-examples-d643cb9ab5c2)
