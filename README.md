# ABHI SIGNALS

Advanced Binary Trading Signal Software

## Features

- EUR/USD
- AUD/USD

- 1 Minute Signals
- 5 Minute Signals

- EMA20
- EMA50
- EMA200

- RSI

- MACD

- ATR Volatility

- Candlestick Patterns

- Candle Psychology

- Support & Resistance

- Breakout Detection

- Fake Breakout Filter

- Multi Timeframe Confirmation

- Session Filter

- Confidence Score

- Daily API Request Tracking

- Auto Stop On Daily Limit Cross

---

# Folder Structure

```text
abhi-signals/

├── app.py
├── config.py
├── data_fetcher.py
├── signal_engine.py
├── request_tracker.py
├── session_filter.py
├── psychology.py
├── support_resistance.py
├── breakout.py
├── multi_timeframe.py
├── requirements.txt
├── render.yaml

├── templates/
│   └── index.html

├── static/
│   ├── style.css
│   └── app.js

├── data/
│   ├── requests.json
│   └── signals.json

└── README.md
```

---

# Twelve Data API Setup

Create account:

https://twelvedata.com

Generate API Key

---

# GitHub Setup

Create new repository:

```text
abhi-signals
```

Upload all files.

Commit:

```bash
git add .
git commit -m "Initial Commit"
git push
```

---

# Render Deployment

Create Web Service

Connect GitHub Repository

---

Build Command

```bash
pip install -r requirements.txt
```

---

Start Command

```bash
gunicorn app:app
```

---

Environment Variable

Key:

```text
TWELVE_DATA_API_KEY
```

Value:

```text
YOUR_API_KEY
```

---

# Test URLs

Health Check

```text
/health
```

Example:

```text
https://your-app.onrender.com/health
```

Response:

```json
{
  "status": "healthy"
}
```

---

Request Status

```text
/api/requests
```

Response:

```json
{
  "used": 0,
  "remaining": 800,
  "limit": 800,
  "limit_crossed": false
}
```

---

Signal Endpoint

```text
/api/signal?pair=EUR/USD&timeframe=1min
```

---

# Supported Timeframes

```text
1min
5min
```

---

# Supported Pairs

```text
EUR/USD
AUD/USD
```

---

# Daily Request Logic

Daily Limit:

```text
800
```

When limit reaches:

```text
DAILY LIMIT CROSSED
```

Software automatically stops requesting signals.

Next UTC day:

```text
Automatic Reset
```

---

# Important Notes

This software generates probability-based signals.

No trading system can reliably guarantee the next candle direction.

Always test using historical data and paper trading before using real money.

---

# Version

ABHI SIGNALS v1.0
