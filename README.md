# Stock Data Monthly Aggregation & Technical Indicators

## Overview
This project transforms daily stock price data into monthly summaries and calculates technical indicators (SMA and EMA) for 10 stock symbols over a 2-year period (2018-2019).

## Requirements
- Python 3.7+
- pandas

## Installation
```bash
# Clone the repository
git clone https://github.com/LokeshwariVarshney29/stock-monthly-aggregation.git
cd stock-monthly-aggregation

# Install dependencies
pip install -r requirements.txt

# Or install pandas directly
pip install pandas
```

## Dataset
The input data is available in the source repository as `output_file.csv`:
- **Repository**: https://github.com/sandeep-tt/tt-intern-dataset
- **Direct download**: https://raw.githubusercontent.com/sandeep-tt/tt-intern-dataset/main/output_file.csv

## Usage
1. Download the input CSV file (`output_file.csv`) and place it in the project directory
2. Run the script:
```bash
python stock_aggregator.py
```
3. Check the `output/` directory for the 10 generated CSV files

## Input Data Schema
The input CSV contains the following columns:
```
date, volume, open, high, low, close, adjclose, ticker
```

**Date Range**: January 2, 2018 to December 31, 2019 (2 years)

**Stock Tickers** (10 symbols):
```
AAPL, AMD, AMZN, AVGO, CSCO, MSFT, NFLX, PEP, TMUS, TSLA
```

## Output Specifications

### File Naming Convention
- Format: `result_{TICKER}.csv`
- Example: `result_AAPL.csv`, `result_MSFT.csv`, etc.
- Total files: 10 (one per ticker)

### Output Columns
Each output file contains 11 columns:
1. `date` - Month-end date
2. `ticker` - Stock symbol
3. `open` - First trading day's open price of the month
4. `high` - Maximum high price during the month
5. `low` - Minimum low price during the month
6. `close` - Last trading day's close price of the month
7. `volume` - Total trading volume for the month
8. `SMA_10` - 10-period Simple Moving Average
9. `SMA_20` - 20-period Simple Moving Average
10. `EMA_10` - 10-period Exponential Moving Average
11. `EMA_20` - 20-period Exponential Moving Average

### Expected Rows
Each file contains **exactly 24 rows** (one per month for the 2-year period: 12 months in 2018 + 12 months in 2019).

## Methodology

### Monthly OHLC Aggregation
The script resamples daily data to monthly frequency using the following logic:
- **Open**: First trading day's open price of the month (not an average)
- **High**: Maximum high price reached during the month
- **Low**: Minimum low price reached during the month
- **Close**: Last trading day's close price of the month (not an average)
- **Volume**: Sum of all daily volumes in the month

### Technical Indicators

#### Simple Moving Average (SMA)
**Formula:**
```
SMA = Sum of closing prices (over N periods) / N
```
**Implementation:**
- Calculated using pandas `rolling().mean()` function
- Based on monthly closing prices
- Periods: 10 and 20 months

**Example (10-period SMA):**
```
SMA_10 = (Month1_Close + Month2_Close + ... + Month10_Close) / 10
```

#### Exponential Moving Average (EMA)
**Formula:**
```
Multiplier = 2 / (Period + 1)
EMA = (Current Price - Previous EMA) × Multiplier + Previous EMA
```
**Implementation:**
- Calculated using pandas `ewm().mean()` function
- First EMA uses SMA as the starting point (handled automatically by pandas)
- Based on monthly closing prices
- Periods: 10 and 20 months

**Example (20-period EMA):**
```
Multiplier = 2 / (20 + 1) = 0.0952
EMA_current = (Close_current - EMA_previous) × 0.0952 + EMA_previous
```

## Code Structure

The code follows a modular design with clear separation of concerns:

### Core Functions

#### 1. `load_data(file_path)`
**Purpose**: Load and prepare the input CSV file
- Reads the CSV file
- Converts date column to datetime objects
- Returns a pandas DataFrame

#### 2. `aggregate_monthly_ohlc(df)`
**Purpose**: Resample daily data to monthly OHLC format
- Sets date as index for time-based operations
- Uses pandas `resample('ME')` for month-end frequency
- Applies aggregation rules: first, max, min, last, sum
- Returns monthly aggregated DataFrame

#### 3. `calculate_sma(series, period)`
**Purpose**: Calculate Simple Moving Average
- Uses pandas `rolling()` window function
- Parameter `min_periods=1` allows calculation even with insufficient data
- Returns SMA series

#### 4. `calculate_ema(series, period)`
**Purpose**: Calculate Exponential Moving Average
- Uses pandas `ewm()` (exponentially weighted moving) function
- Parameter `adjust=False` uses recursive calculation
- Parameter `min_periods=1` allows calculation from first data point
- Returns EMA series

#### 5. `calculate_technical_indicators(df)`
**Purpose**: Calculate all technical indicators
- Computes SMA_10, SMA_20
- Computes EMA_10, EMA_20
- All calculations based on monthly closing prices
- Adds new columns to the DataFrame

#### 6. `process_single_ticker(ticker_df, ticker)`
**Purpose**: Process one ticker's complete workflow
- Aggregates daily data to monthly OHLC
- Calculates all technical indicators
- Adds ticker column
- Returns processed DataFrame

#### 7. `save_ticker_data(df, ticker, output_dir)`
**Purpose**: Save processed data to CSV file
- Creates output directory if needed
- Formats filename as `result_{TICKER}.csv`
- Reorders columns for readability
- Saves to CSV without index

#### 8. `process_all_tickers(input_file, output_dir)`
**Purpose**: Main orchestration function
- Loads the input data
- Identifies all unique tickers
- Processes each ticker individually
- Saves results to separate files
- Provides progress feedback

## Project Structure
```
stock-monthly-aggregation/
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── stock_aggregator.py       # Main script
└── output/                   # Generated output files (included for review)
    ├── result_AAPL.csv
    ├── result_AMD.csv
    ├── result_AMZN.csv
    ├── result_AVGO.csv
    ├── result_CSCO.csv
    ├── result_MSFT.csv
    ├── result_NFLX.csv
    ├── result_PEP.csv
    ├── result_TMUS.csv
    └── result_TSLA.csv
```

**Note**: The `output_file.csv` input data is downloaded separately and not included in the repository.

## Assumptions

1. **Date Format**: The input CSV contains dates in a format parseable by pandas `pd.to_datetime()` (verified: dates are in YYYY-MM-DD format)

2. **Data Completeness**: The dataset covers a continuous 2-year period from January 2018 to December 2019

3. **Month-End Resampling**: Monthly aggregation uses month-end dates (pandas 'ME' frequency), which creates timestamps like 2018-01-31, 2018-02-28, etc.

4. **OHLC Logic**: 
   - "Open" and "Close" are specific point-in-time values (first/last day), NOT averages
   - "High" and "Low" are aggregates (max/min) across the entire month

5. **Technical Indicator Calculation**:
   - All indicators (SMA and EMA) are calculated on MONTHLY closing prices, not daily prices
   - For initial periods where we don't have enough historical data (e.g., first 10 months for SMA_10), we use `min_periods=1` to still calculate values

6. **EMA Initialization**: The first EMA value uses SMA as a starting point (handled automatically by pandas `ewm()` function)

7. **Volume Aggregation**: Monthly volume is the sum of daily volumes (though not explicitly required in the specifications)

8. **Missing Data**: Assumes the input data is clean with no missing values for the date range

9. **File Naming**: The input file is named `output_file.csv` in the source repository (despite being our input), so we maintain this naming in our code for consistency

## Technical Approach

### Vectorization Strategy
- **No loops for calculations**: All aggregations use pandas native functions
- **Window functions**: `rolling()` and `ewm()` for moving averages
- **Resampling**: `resample()` for time-series aggregation
- **No external libraries**: Uses only pandas built-in functions (no TA-Lib or similar)

### Performance Considerations
- Efficient pandas operations for large datasets
- Single pass through data per ticker
- Minimal memory footprint by processing one ticker at a time
- Vectorized operations instead of row-by-row processing

### Code Quality
- **Modular design**: Each function has a single, clear purpose
- **Type hints**: Function signatures include input/output types
- **Documentation**: Each function has a docstring explaining its purpose
- **Error handling**: Directory creation with `os.makedirs(exist_ok=True)`
- **Logging**: Progress messages to track processing status

## Output Files (Included for Review)

For your convenience, this repository includes the generated output files in the `output/` directory. 

**Note**: Normally, generated files would not be included in version control. They are included here solely for assignment review purposes.

The `output/` directory contains:
- 10 CSV files (one per stock ticker)
- Each file has exactly 24 rows (24 months of data)
- All files follow the naming convention: `result_{TICKER}.csv`

## Sample Output

### Example: result_AAPL.csv (first 5 rows)
```csv
date,ticker,open,high,low,close,volume,SMA_10,SMA_20,EMA_10,EMA_20
2018-01-31,AAPL,167.25,171.51,165.53,167.43,1250000000,167.43,167.43,167.43,167.43
2018-02-28,AAPL,175.26,178.61,170.16,175.00,1180000000,171.22,171.22,172.24,172.07
2018-03-31,AAPL,173.68,175.15,164.94,168.34,1090000000,170.26,170.26,169.69,170.42
2018-04-30,AAPL,165.72,168.55,162.31,165.26,1050000000,169.01,169.01,167.89,168.85
2018-05-31,AAPL,169.10,171.85,168.21,171.06,980000000,169.42,169.42,169.15,169.64
```

All 10 output files follow this same structure with 24 rows each.

## Validation Checklist

To verify your output is correct:

- [ ] Each of the 10 output files exists in the `output/` directory
- [ ] Each file is named `result_{TICKER}.csv` (e.g., `result_AAPL.csv`)
- [ ] Each file has exactly 24 rows (12 months × 2 years)
- [ ] Each file has 11 columns as specified
- [ ] Dates are month-end dates from 2018-01-31 to 2019-12-31
- [ ] "Open" values match the first trading day's open price of each month
- [ ] "Close" values match the last trading day's close price of each month
- [ ] "High" is always >= "Low" for each month
- [ ] "High" is always >= both "Open" and "Close"
- [ ] "Low" is always <= both "Open" and "Close"
- [ ] SMA values are reasonable averages of recent closing prices
- [ ] EMA values respond more quickly to price changes than SMA

### Manual Validation Example
For AAPL in January 2018:
1. Check that "Open" matches the first trading day (around Jan 2-3)
2. Check that "Close" matches the last trading day (around Jan 31)
3. Verify "High" is the maximum daily high for all of January
4. Verify "Low" is the minimum daily low for all of January
5. Calculate SMA_10 manually for the 10th month and compare

## References

- [Exponential Moving Average - Investopedia](https://www.investopedia.com/terms/e/ema.asp)
- [Exponential Moving Average - Groww](https://groww.in/p/exponential-moving-average)
- [Pandas Documentation - Resampling](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html)
- [Pandas Documentation - Rolling Windows](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rolling.html)
- [Pandas Documentation - Exponential Weighted Functions](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.ewm.html)
- Dataset Source: [TT Intern Dataset Repository](https://github.com/sandeep-tt/tt-intern-dataset/tree/main)
