import sqlite3
import pandas as pd
from datetime import datetime
import os

def format_date(date_str):
    """Format date string to match table names (e.g., 1092023 -> 01092023)."""
    try:
        # Convert to string if it's not already
        date_str = str(date_str)
        # Add leading zero if needed
        if len(date_str) == 7:
            return '0' + date_str
        return date_str
    except:
        return date_str

def fetch_option_prices():
    """Fetch option prices at 3:25 PM for selected strikes."""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(base_dir, 'data')
    reports_dir = os.path.join(base_dir, 'reports')
    
    # Read strike selection data
    try:
        strike_data = pd.read_csv(os.path.join(reports_dir, 'strike_selection.csv'))
        strike_data.set_index('date', inplace=True)
    except FileNotFoundError:
        print("Error: strike_selection.csv not found. Please run 03_select_strike.py first.")
        return
    
    # Connect to options database
    conn = sqlite3.connect(os.path.join(data_dir, 'OPT.db'))
    cursor = conn.cursor()
    
    # Initialize results DataFrame
    results = pd.DataFrame(index=strike_data.index)
    
    # Process each day
    for date in strike_data.index:
        try:
            # Format date for table name
            table_date = format_date(date)
            
            atm_strike = int(strike_data.loc[date, 'atm_strike'])
            hedge_strike = int(strike_data.loc[date, 'hedge_strike'])
            direction = strike_data.loc[date, 'direction']
            
            # Query for ATM option price (CE for UP, PE for DOWN)
            atm_query = f"""
            SELECT close as price
            FROM '{table_date}'
            WHERE time = '15:25:00'
            AND strike = {atm_strike}
            AND instrument_type = '{"CE" if direction == "UP" else "PE"}'
            """
            
            # Query for hedge option price (PE for UP, CE for DOWN)
            hedge_query = f"""
            SELECT close as price
            FROM '{table_date}'
            WHERE time = '15:25:00'
            AND strike = {hedge_strike}
            AND instrument_type = '{"PE" if direction == "UP" else "CE"}'
            """
            
            # Execute queries
            cursor.execute(atm_query)
            atm_price = cursor.fetchone()
            
            cursor.execute(hedge_query)
            hedge_price = cursor.fetchone()
            
            # Store results
            results.loc[date, 'atm_strike'] = atm_strike
            results.loc[date, 'hedge_strike'] = hedge_strike
            results.loc[date, 'direction'] = direction
            results.loc[date, 'atm_price'] = atm_price[0] if atm_price else None
            results.loc[date, 'hedge_price'] = hedge_price[0] if hedge_price else None
            
        except (sqlite3.OperationalError, KeyError) as e:
            print(f"Error processing date {date}: {str(e)}")
            continue
    
    conn.close()
    
    # Drop rows with missing prices
    results = results.dropna(subset=['atm_price', 'hedge_price'])
    
    # Calculate total premium
    results['total_premium'] = results['atm_price'] + results['hedge_price']
    
    # Save results
    results.to_csv(os.path.join(reports_dir, 'option_prices.csv'))
    
    # Print summary
    print("\nOption Price Analysis:")
    print("=====================")
    print(f"Total days processed: {len(results)}")
    print("\nAverage Premiums by Direction:")
    print(results.groupby('direction')[['atm_price', 'hedge_price', 'total_premium']].mean())
    print("\nSample of first 5 days:")
    print(results.head())
    
    return results

if __name__ == "__main__":
    fetch_option_prices() 