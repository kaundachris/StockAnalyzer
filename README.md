# Stock Analyzer

A Flask web application for fundamental analysis of stocks listed on US exchanges. Users can search for any company by name or ticker, view key financial metrics, and — if registered — save and track searches over time.

**Live Demo:** https://youtu.be/okp5wamPM60

---

## Features

- Search by company name or ticker symbol
- Real-time financial data via Yahoo Finance
- Dynamic explanations of each financial metric
- User authentication (register, login, logout)
- Search history with update and delete functionality
- Sortable history table by any financial metric
- Searches available to guests — no account required to explore

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | PostgreSQL (via psycopg2) |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| Data | yfinance (Yahoo Finance) |
| Auth | bcrypt |
| Deployment | Render (gunicorn) |

---

## Project Structure
```
stock-analyzer/
│
├── app.py                  # Flask routes and core application logic
├── stockdata.py            # Stock data retrieval and processing
├── company_check.py        # Company name to ticker resolution
├── requirements.txt        # Python dependencies
├── render.yaml             # Render deployment configuration
├── .env                    # Environment variables (not committed)
├── .gitignore
│
├── templates/
│   ├── base.html           # Shared layout
│   ├── index.html          # Search page
│   ├── results.html        # Stock analysis results
│   ├── history.html        # Saved search history
│   ├── login.html          # Login page
│   └── register.html       # Registration page
│
└── static/
    ├── index.css           # Stylesheet
    └── index.js            # Dynamic footer year
```

---

## Database Schema

### `users`
| Column | Type | Notes |
|---|---|---|
| id | SERIAL | Primary key |
| username | TEXT | Unique, not null |
| password_hash | TEXT | bcrypt hash |

### `searches`
| Column | Type | Notes |
|---|---|---|
| id | SERIAL | Primary key |
| user_id | INTEGER | Foreign key → users.id |
| ticker | TEXT | Stock ticker symbol |
| long_name | TEXT | Company full name |
| industry | TEXT | Industry classification |
| forward_pe | REAL | Forward Price/Earnings ratio |
| earnings_growth | REAL | Year-over-year earnings growth |
| profit_margins | REAL | Net profit margin |
| market_cap | REAL | Market capitalisation |
| book_value | REAL | Book value per share |
| price_book | REAL | Price-to-Book ratio |
| quick_ratio | REAL | Quick ratio |
| current_ratio | REAL | Current ratio |
| free_cashflow | REAL | Free cash flow |

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- PostgreSQL database
- A `DATABASE_URL` connection string

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/your-username/stock-analyzer.git
cd stock-analyzer
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```
DATABASE_URL=postgresql://username:password@localhost:5432/stockanalyzer
SECRET_KEY=your-secret-key-here
```

To generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```

5. **Run the application**
```bash
python app.py
```

The app will be available at `http://localhost:5000`.

---

## Deployment (Render)

The app is configured for deployment on [Render](https://render.com) via `render.yaml`.

Set the following environment variables in your Render dashboard:
- `DATABASE_URL` — your PostgreSQL connection string
- `SECRET_KEY` — a securely generated random string

The database tables are created automatically on startup via `initialize_db()`.

---

## Financial Metrics Explained

| Metric | What It Measures |
|---|---|
| Forward P/E | Expected earnings relative to price — lower may indicate better value |
| Earnings Growth | Year-over-year growth in earnings per share |
| Profit Margin | Percentage of revenue retained as profit |
| Price-to-Book | Share price relative to book value — lower may indicate undervaluation |
| Quick Ratio | Ability to cover short-term liabilities without selling inventory |
| Current Ratio | Broader measure of short-term financial health |
| Free Cash Flow | Cash remaining after capital expenditure |

---

## Security

- Passwords hashed with **bcrypt** before storage — plaintext is never stored
- Parameterised queries throughout — protected against SQL injection
- Column whitelisting for sort parameters — dynamic SQL is never built from raw user input
- Session cleared on login — prevents session fixation attacks
- Credentials stored in environment variables — never hardcoded

---

## Future Improvements

- Ascending/descending sort toggle on history table
- Technical analysis metrics (moving averages, RSI)
- CSV export of search history
- Mobile-responsive design
- Real-time price updates