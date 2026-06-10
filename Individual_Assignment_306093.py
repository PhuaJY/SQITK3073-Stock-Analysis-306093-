# QUESTION 1: Bursa Malaysia Stock Analysis

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# 1. Defining the initial variables
INVESTMENT_CAPITAL = 1000.00
tickers = ['1155.KL', '5347.KL', '6947.KL', '5225.KL', '5211.KL']

# Defining the recent 1-month period
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

# Creating the empty list to hold the data records
portfolio_data = []

# 2. Looping through each ticker to fetch data and calculate the metrics
for ticker in tickers:
    stock = yf.Ticker(ticker)
    
    # Fetching the trading data from 1  month ago
    hist = stock.history(period="1mo")
    
    # Ensuring that the data is enough to compare yesterday and today
    if len(hist) >= 2:
        # Extracting the closing prices
        yesterday_close = hist['Close'].iloc[-2]
        today_close = hist['Close'].iloc[-1]
        
        # Calculating the required metrics
        daily_return = today_close - yesterday_close
        
        # Calculating the shares purchasable (by using integer division for whole shares)
        shares_purchasable = int(INVESTMENT_CAPITAL / yesterday_close)
        
        # Calculating the overall returns
        est_total_return = daily_return * shares_purchasable
        return_percentage = (est_total_return / INVESTMENT_CAPITAL) * 100
        
        # 3. Appending the calculated data as a new "row" in the list
        portfolio_data.append({
            'Ticker': ticker,
            'Yesterday Closing Price': round(yesterday_close, 3),
            'Today Closing Price': round(today_close, 3),
            'Daily Return': round(daily_return, 3),
            'Shares Purchasable': shares_purchasable,
            'Estimated Total Return': round(est_total_return, 3),
            'Return Percentage': round(return_percentage, 3)
        })

# 4. Converting the list of records into a pandas DataFrame 
df = pd.DataFrame(portfolio_data)
print("Question 1: Bursa Malaysia Stock Analysis")
print("-" * 75)
print(df.to_string(index=False))



# QUESTION 2)a): pandas Slicing

# Only selecting the specific columns required 
summary_df = df[['Ticker', 'Yesterday Closing Price', 'Today Closing Price', 
                 'Estimated Total Return', 'Return Percentage']].copy()

# Renaming the columns 
summary_df = summary_df.rename(columns={
    'Yesterday Closing Price': 'Previous Closing Price',
    'Today Closing Price': 'Latest Closing Price'
})

print("\nQuestion 2(a): Portfolio Summary Table")
print("-" * 75)
print(summary_df.to_string(index=False))


# QUESTION 2)b): GroupBy Analysis

# 1. Creating a function to classify the return of percentages
def categorize_performance(return_pct):
    if return_pct < 0:
        return 'Negative Return'
    elif return_pct <= 2:
        return 'Moderate Return'
    else:
        return 'High Return'

# 2. Applying the function to create a new "Performance Category" column
df['Performance Category'] = df['Return Percentage'].apply(categorize_performance)

# 3. Using the groupby() function to calculate the average return for each category
grouped_df = df.groupby('Performance Category')['Estimated Total Return'].mean().reset_index()

# Renaming the output column to make the table look good
grouped_df = grouped_df.rename(columns={'Estimated Total Return': 'Average Estimated Return (RM)'})

print("\nQuestion 2(b): GroupBy Analysis")
print("-" * 75)
print(grouped_df.to_string(index=False))



# QUESTION 3: Data Visualization

import matplotlib.pyplot as plt

# Chart 1: Closing Price Trend
# Downloading the daily closing prices for the last month for all 5 stocks
trend_data = yf.download(tickers, period="1mo", progress=False)['Close']

plt.figure(figsize=(10, 5))
for ticker in tickers:
    plt.plot(trend_data.index, trend_data[ticker], linewidth=2, label=ticker)

plt.title('1-Month Closing Price Trend of Selected Bursa Malaysia Stocks')
plt.xlabel('Date')
plt.ylabel('Closing Price (RM)')
plt.legend(title="Stock Tickers")
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show() # This will open up the first chart window

# Chart 2: Portfolio Performance Comparison
# Using a bar chart to compare the Return Percentage of each of the stock
plt.figure(figsize=(10, 5))

# Creating colors: Green for positive returns, Red for negative returns
colors = ['green' if val >= 0 else 'red' for val in df['Return Percentage']]
bars = plt.bar(df['Ticker'], df['Return Percentage'], color=colors)

plt.title('Return Percentage Comparison (RM1,000 Initial Capital)')
plt.xlabel('Stock Ticker')
plt.ylabel('Return Percentage (%)')
plt.axhline(0, color='black', linewidth=1) # Adds a baseline at 0%

# Adding the exact percentage labels on top/bottom of each of the bar
for bar in bars:
    yval = bar.get_height()
    vertical_offset = 0.5 if yval >= 0 else -1.5
    plt.text(bar.get_x() + bar.get_width()/2, yval + vertical_offset, 
             f'{round(yval, 2)}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.show() # This will open up the second chart window