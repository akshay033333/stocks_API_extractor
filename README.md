# Stock API Extractor

A Python script that extracts stock ticker data from the Polygon API and saves it to CSV files with pagination support and rate limiting.

## Features

- 🔑 **Secure API Key Management**: Uses environment variables for API key storage
- 📄 **Pagination Support**: Automatically fetches all available data using `next_url`
- ⏱️ **Rate Limiting**: Handles API rate limits with intelligent retry logic
- 📊 **CSV Export**: Saves data to timestamped CSV files
- 🛡️ **Error Handling**: Robust error handling for network and API errors
- 📈 **Progress Tracking**: Real-time progress updates during data fetching

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stocks_API_extractor
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv pyenv
   source pyenv/bin/activate  # On Windows: pyenv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```
   POLYGON_API_KEY=your_api_key_here
   ```

## Usage

### 1. Data Extraction

Run the script to fetch all available stock tickers:

```bash
python Script.py
```

The script will:
- Load your API key from the `.env` file
- Fetch stock data page by page from Polygon API
- Handle rate limiting automatically
- Save all data to a timestamped CSV file

### 2. Data Visualization

Launch the Streamlit web app to explore and analyze your data:

```bash
streamlit run app.py
```

The web app provides:
- 📊 Interactive data visualization
- 🔍 Advanced filtering and search
- 📈 Market and exchange analytics
- 📋 Data export capabilities
- 📱 Responsive design for all devices

## Output

The script generates CSV files with the following format:
- **Filename**: `stock_tickers_YYYYMMDD_HHMMSS.csv`
- **Content**: All available stock ticker data including:
  - `ticker`: Stock symbol
  - `name`: Company name
  - `market`: Market type
  - `primary_exchange`: Exchange
  - `type`: Security type
  - `currency_name`: Currency
  - And more...

## API Rate Limits

The script automatically handles Polygon API rate limits:
- Waits 60 seconds when rate limited
- Adds small delays between requests
- Retries failed requests automatically

## Requirements

- Python 3.7+
- Polygon API key
- Internet connection

## Dependencies

- `requests`: HTTP library for API calls
- `python-dotenv`: Environment variable management
- `streamlit`: Web app framework for data visualization
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive plotting library

## Example Output

```
Loading API key from .env file...
API Key loaded successfully
✅ API key is ready to use!
Fetching stock data from Polygon API...
📄 Fetching page 1...
   ✅ Added 1000 tickers from page 1
   🔄 Next page available: https://api.polygon.io/v3/reference/tickers?cursor...
...
✅ Successfully fetched 11739 total stock tickers across 15 pages
✅ Data saved to stock_tickers_20250914_091850.csv
📊 Total records: 11739
```

## License

This project is open source and available under the MIT License.
