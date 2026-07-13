# Stock Analyzer

Stock Analyzer is a Flask-based web application that lets users explore basic fundamental stock data and save their research over time. The project is designed as a portfolio piece that demonstrates both software engineering fundamentals and practical finance knowledge.

**Live Demo:** https://youtu.be/okp5wamPM60

## What this project does

Users can search for a company by name or ticker symbol and view core financial metrics such as:

- Forward P/E
- Earnings growth
- Profit margin
- Market capitalization
- Book value
- Price-to-book ratio
- Quick ratio
- Current ratio
- Free cash flow

The app also provides plain-language context for each metric so the analysis feels more accessible to non-technical users.

## Core features

- Company lookup by ticker or company name
- Retrieval of live financial data through Yahoo Finance
- Fundamental analysis views for key valuation and profitability metrics
- User accounts with registration, login, password reset, and logout
- Persistent search history for authenticated users
- Update and delete actions for saved research entries
- Sortable history data for comparing financial metrics over time
- Guest access for basic exploration without creating an account

## Why this is a strong engineering showcase

This project goes beyond a simple demo app. It combines several common software engineering concerns in one product:

- Backend development with Flask and Python
- External API integration and data handling
- Authentication, session management, and secure password storage
- Database design and persistence with PostgreSQL
- Input validation and protection against common web vulnerabilities
- Deployment configuration for a production-style hosting environment

## Technical stack

- Backend: Python, Flask
- Database: PostgreSQL
- Frontend: HTML, CSS, JavaScript, Jinja2
- Data source: Yahoo Finance via yfinance
- Authentication: bcrypt
- Deployment: Render with Gunicorn

## Project structure

- app.py: Flask routes, session handling, authentication flow, and database operations
- stockdata.py: Stock data retrieval and financial metric transformation
- company_check.py: Company name-to-ticker resolution
- templates/: User-facing HTML templates
- static/: CSS and JavaScript assets

## Finance angle

The app is intentionally centered around fundamental analysis rather than speculative trading. It highlights concepts that matter in investment research:

- Valuation metrics such as P/E and price-to-book
- Profitability and growth indicators
- Liquidity and balance sheet health
- Cash flow as a measure of business quality

That makes the project useful both as a software portfolio item and as a demonstration of financial literacy.

## Setup

### Prerequisites
- Python 3.10+
- PostgreSQL
- Environment variables for DATABASE_URL and SECRET_KEY

### Local development

```bash
git clone <repo-url>
cd stock-analyzer
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or .\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python app.py
```

Create a .env file with:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/stockanalyzer
SECRET_KEY=your-secret-key
```

## Notes

This is a portfolio-scale web application rather than a full trading platform. The current scope focuses on stock lookup, fundamental data presentation, user accounts, and saved research history.
