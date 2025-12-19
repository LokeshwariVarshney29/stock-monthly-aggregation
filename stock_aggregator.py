import pandas as pd
import os

# Load the stock data from CSV file.
def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv('output_file.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

# Aggregate daily stock data to monthly OHLC format.
def aggregate_monthly_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    # Set date as index for resampling
    df = df.set_index('date').sort_index()
    # Define aggregation rules
    agg_rules = {
        'open': 'first',      # First day's open price
        'high': 'max',        # Maximum high during the month
        'low': 'min',         # Minimum low during the month
        'close': 'last',      # Last day's close price
        'volume': 'sum'       # Total volume
    }
    # Resample to monthly frequency using month-end
    monthly_df = df.resample('ME').agg(agg_rules)
    # Reset index to make date a column again
    monthly_df = monthly_df.reset_index()
    return monthly_df

# Calculate Simple Moving Average.
# Formula: SMA = Sum of closing prices (over N periods) / N
def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    return series.rolling(window=period, min_periods=1).mean()

# Calculate Exponential Moving Average.
'''Formula: 
- Multiplier = 2 / (period + 1)
- EMA = (Current Price - Previous EMA) * Multiplier + Previous EMA
- First EMA uses SMA as starting point '''
def calculate_ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False, min_periods=1).mean()

# Calculate all technical indicators (SMA and EMA) based on monthly closing prices.
def calculate_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # Calculate Simple Moving Averages
    df['SMA_10'] = calculate_sma(df['close'], 10)
    df['SMA_20'] = calculate_sma(df['close'], 20)
    # Calculate Exponential Moving Averages
    df['EMA_10'] = calculate_ema(df['close'], 10)
    df['EMA_20'] = calculate_ema(df['close'], 20)    
    return df

# Process a single ticker's data: aggregate monthly and calculate indicators.
def process_single_ticker(ticker_df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    # Aggregate to monthly OHLC
    monthly_df = aggregate_monthly_ohlc(ticker_df)
    # Calculate technical indicators
    monthly_df = calculate_technical_indicators(monthly_df)
    # Add ticker column
    monthly_df['ticker'] = ticker    
    return monthly_df

# Save processed data for a single ticker to CSV file.
def save_ticker_data(df: pd.DataFrame, ticker: str, output_dir: str = 'output'):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # Define output file path
    output_file = os.path.join(output_dir, f'result_{ticker}.csv')
    # Reorder columns for better readability
    columns_order = ['date', 'ticker', 'open', 'high', 'low', 'close', 
                     'volume', 'SMA_10', 'SMA_20', 'EMA_10', 'EMA_20']
    df = df[columns_order]
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Saved {ticker} data to {output_file} ({len(df)} rows)")

# Main processing function: loads data, processes each ticker, and saves results.
def process_all_tickers(input_file: str, output_dir: str = 'output'):
    print("Loading data...")
    df = load_data(input_file)
    # Get unique tickers
    tickers = df['ticker'].unique()
    print(f"Found {len(tickers)} tickers: {', '.join(tickers)}")
    print("\nProcessing each ticker...")
    for ticker in tickers:
        # Filter data for current ticker
        ticker_df = df[df['ticker'] == ticker].copy()
        # Process ticker data
        monthly_df = process_single_ticker(ticker_df, ticker)
        # Save to file
        save_ticker_data(monthly_df, ticker, output_dir)
    print(f"\nProcessing complete! All files saved to '{output_dir}/' directory")

if __name__ == "__main__":
    INPUT_FILE = 'output_file.csv'
    OUTPUT_DIR = 'output'
    process_all_tickers(INPUT_FILE, OUTPUT_DIR)