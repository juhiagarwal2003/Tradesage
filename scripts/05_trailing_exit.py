import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

def format_date(date_str):
    """Format date string to match table names (e.g., 1092023 -> 01092023)."""
    try:
        # Convert to datetime for consistent formatting
        date = datetime.strptime(str(date_str), '%d%m%Y')
        return date.strftime('%d%m%Y')
    except:
        return str(date_str)

def get_next_trading_day(conn, date_str):
    """Get the next available trading day from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    all_dates = [table[0] for table in cursor.fetchall()]
    
    try:
        current_idx = all_dates.index(format_date(date_str))
        if current_idx < len(all_dates) - 1:
            return all_dates[current_idx + 1]
    except ValueError:
        pass
    return None

def calculate_trailing_exit(prices, direction, window=3):
    """
    Calculate trailing exit based on 3-minute high/low.
    
    Args:
        prices (pd.DataFrame): DataFrame with time and close price columns
        direction (str): 'UP' or 'DOWN' indicating trade direction
        window (int): Number of minutes for trailing window
        
    Returns:
        tuple: (exit_price, exit_time, entry_price)
    """
    if len(prices) < window:
        return None, None, None
    
    # Get entry price (first price of the day)
    entry_price = prices.iloc[0]['close']
    
    # For UP trades, we trail below the low
    # For DOWN trades, we trail above the high
    price_col = 'low' if direction == 'UP' else 'high'
    comparison = (lambda x, y: x > y) if direction == 'UP' else (lambda x, y: x < y)
    
    # Calculate rolling extreme
    prices['rolling_extreme'] = prices[price_col].rolling(window=window).min() if direction == 'UP' else prices[price_col].rolling(window=window).max()
    
    # Initialize variables
    current_extreme = float('inf') if direction == 'UP' else float('-inf')
    exit_price = None
    exit_time = None
    
    # Find the first price that crosses the trailing stop
    for i in range(window, len(prices)):
        current_price = prices.iloc[i]['close']
        prev_extreme = prices['rolling_extreme'].iloc[i-1]
        
        if comparison(prev_extreme, current_extreme):
            current_extreme = prev_extreme
        
        if comparison(current_price, current_extreme):
            exit_price = current_price
            exit_time = prices.iloc[i]['time']
            break
    
    # If no exit found, use the last price
    if exit_price is None:
        exit_price = prices.iloc[-1]['close']
        exit_time = prices.iloc[-1]['time']
    
    return exit_price, exit_time, entry_price

def process_trailing_exits():
    """Process trailing exits for all trading days."""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(base_dir, 'data')
    reports_dir = os.path.join(base_dir, 'reports')
    
    # Read option prices data
    try:
        option_data = pd.read_csv(os.path.join(reports_dir, 'option_prices.csv'))
        option_data.set_index('date', inplace=True)
    except FileNotFoundError:
        print("Error: option_prices.csv not found. Please run 04_fetch_option_prices.py first.")
        return
    
    # Connect to spot database
    conn = sqlite3.connect(os.path.join(data_dir, 'SPOT.db'))
    
    # Initialize results DataFrame
    results = pd.DataFrame(index=option_data.index)
    
    # Process each day
    for date in option_data.index:
        try:
            # Get next trading day
            next_date = get_next_trading_day(conn, date)
            if next_date is None:
                print(f"Warning: No next trading day found for {date}")
                continue
            
            # Query next day's morning prices
            query = f"""
            SELECT time, open, high, low, close
            FROM '{next_date}'
            WHERE time >= '09:15:00'
            AND time <= '09:30:00'
            ORDER BY time
            """
            
            # Get price data
            prices = pd.read_sql_query(query, conn)
            
            if not prices.empty:
                # Get direction for this trade
                direction = option_data.loc[date, 'direction']
                
                # Calculate trailing exit
                exit_price, exit_time, spot_entry = calculate_trailing_exit(prices, direction)
                
                if exit_price is not None:
                    # Store results
                    results.loc[date, 'option_premium'] = option_data.loc[date, 'total_premium']
                    results.loc[date, 'spot_entry'] = spot_entry
                    results.loc[date, 'spot_exit'] = exit_price
                    results.loc[date, 'exit_time'] = exit_time
                    results.loc[date, 'direction'] = direction
        
        except (sqlite3.OperationalError, KeyError) as e:
            print(f"Error processing date {date}: {str(e)}")
            continue
    
    conn.close()
    
    # Drop rows with missing data
    results = results.dropna()
    
    # Calculate P&L
    results['spot_points'] = results.apply(
        lambda row: row['spot_exit'] - row['spot_entry'] if row['direction'] == 'UP' else row['spot_entry'] - row['spot_exit'],
        axis=1
    )
    
    # Save results
    results.to_csv(os.path.join(reports_dir, 'trailing_exits.csv'))
    
    # Print summary
    print("\nTrailing Exit Analysis:")
    print("======================")
    print(f"Total days processed: {len(results)}")
    
    print("\nAverage Exit Times by Direction:")
    results['minutes_after_open'] = results['exit_time'].apply(
        lambda x: (datetime.strptime(x, '%H:%M:%S') - datetime.strptime('09:15:00', '%H:%M:%S')).total_seconds() / 60
    )
    avg_times = results.groupby('direction')['minutes_after_open'].mean()
    print(avg_times)
    
    print("\nProfitability Analysis:")
    print("\nAverage Spot Points by Direction:")
    print(results.groupby('direction')['spot_points'].mean())
    print("\nAverage Option Premium by Direction:")
    print(results.groupby('direction')['option_premium'].mean())
    
    print("\nSample of first 5 days:")
    print(results[['option_premium', 'spot_entry', 'spot_exit', 'spot_points', 'direction', 'exit_time']].head())
    
    return results

if __name__ == "__main__":
    process_trailing_exits() 