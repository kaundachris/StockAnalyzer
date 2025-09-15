# Stock Analyzer

#### Video Demo:  <URL HERE>

## Project Overview
Stock Analyzer is a web application that helps users analyze stock fundamentals for companies listed on US stock exchanges. It provides key financial metrics and ratios to assist in investment decision-making, and provides a description of the importance of each financial metric and ratio. This allows the user with little to no understanding of fundamental analysis to know why each metric matters.

It allows for the results to be dynamically inserted into the results of each search, allowing for relevant results nad explanations 

### Key Features
- Real-time stock data retrieval.
- Dynamic explanations to the stock's fundamental metrics.
- User authentication system.
- Historical search tracking, with allowance for updates to previous searches to check for new data.
- Fundamental analysis metrics including:
  - Forward P/E Ratio,
  - Earnings Growth,
  - Profit Margins,
  - Price-to-Book Ratio,
  - Quick Ratios,
  - Current Ratios,
  - Free Cash Flow.

## Technologies Used

### Languages
- Python 3.13.7
- HTML/CSS
- JavaScript

### Main Libraries
- Flask - Web framework
- yfinance - Yahoo Finance API wrapper
- SQLite3 - Database management
- bcrypt - Password hashing
- Jinja2 - Template engine

## Project Structure

### Core Files
- `app.py` - Main application file containing Flask routes and core logic of the website.
- `stockdata.py` - Used to retrieve the stock data in a concise format. Stock data is retrived using the yfinance module.
- `requirements.txt` - Contains a list of all the project dependencies.

### Templates
- `base.html` - Base template that other templates extend from.
- `index.html` - Homepage which allows a user - loggen in or not - to serach for a stock of choice. This was a concious choice as I think people might be averse to signing up for something they only use once in a while. This way, a person can search for a stock quickly, without going through the hassle of logging in.
- `login.html` - User login page - allows the user to save their searches and view the history of their searches. 
- `register.html` - New user registration page.
- `history.html` - Displays user's previous stock queries - conditional on the user being logged in.
- `results.html` - Shows detailed stock analysis results.

### Static Files
- `static/index.css` - Main stylesheet for the application.
- `static/index.js` - Client-side JavaScript functionality - I use this to get the year dynamically.

### Database
- `instance/stockanalyzer.db` - SQLite database file (auto-generated)

## File Descriptions

#### Backend
- `app.py`: Contains all Flask routes, database interactions, and core application logic including user authentication and storage of the user's stock data searches in their database.
- `stockdata.py`: Handles all interactions with the yfinance API, processes raw stock data, and calculates financial metrics.

#### Frontend
- `base.html`: Contains the basic HTML structure, navigation, and footer shared across all pages.
- `index.html`: Main search interface where users can input stock tickers.
- `login.html`: User authentication interface.
- `register.html`: New user registration interface.
- `history.html`: Displays a table of previous stock searches with update functionality.
- `results.html`: Detailed view of stock analysis with key metrics and explanations.

#### Static Assets
- `index.css`: Handles all styling including dark theme, responsive design, and table layouts.
- `index.js`: Manages dynamic content updates particularly for the date functionality in the page's footer

## Setup & Installation
1. Clone the repository
2. Install required packages:
```bash
pip install -r requirements.txt
```
3. Set up environment variables:
```bash
export SECRET_KEY="your_secret_key"
```
4. Run the application:
```bash
python app.py
```

## Database Structure
The application uses SQLite with two main tables:
- users: Stores user authentication data
- searches: Stores historical stock queries

## Security Features
- Password hashing using bcrypt
- Session-based authentication
- Input validation and sanitization

## API Integration
### yfinance API
- Retrieves real-time stock data
- Caches responses to minimize API calls
- Handles rate limiting automatically
- Error handling for invalid tickers

## User Experience
### Non-authenticated Users
- Can search for stock information
- View detailed analysis
- Access to all fundamental metrics

### Authenticated Users
- All features available to non-authenticated users
- Search history tracking
- Ability to update previous searches
- Data persistence across sessions

## Error Handling
- Invalid stock ticker validation
- API failure graceful degradation
- Database connection error recovery
- User input sanitization

## Performance Optimizations
- Client-side caching
- Minimal API calls through data caching
- Efficient database queries
- Compressed static assets

## Testing
```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/
```

## Development
### Local Development Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### Database Migrations
```bash
# Initialize the database
flask db init

# Create new migration
flask db migrate

# Apply migration
flask db upgrade
```

## Troubleshooting
Common issues and solutions:
1. API Rate Limiting
2. Database Connection Issues
3. Authentication Errors
4. Data Caching Problems

## Future Enhancements
- Technical analysis integration
- Real-time price updates
- Export functionality
- Mobile responsive design
- Dark/Light theme toggle
