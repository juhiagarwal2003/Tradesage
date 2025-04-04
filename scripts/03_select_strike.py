import pandas as pd
import numpy as np
from datetime import datetime
import os

def select_strikes(spot_price, strike_interval=100):
    """
    Select ATM and hedge strike prices based on spot price.
    
    Args:
        spot_price (float): Current spot price
        strike_interval (int): Interval between strike prices
        
    Returns:
        tuple: (atm_strike, hedge_strike)
    """
    # Calculate nearest strike price
    atm_strike = round(spot_price / strike_interval) * strike_interval
    
    # Select hedge strike (one strike above for upward movement)
    hedge_strike = atm_strike + strike_interval
    
    return atm_strike, hedge_strike

def process_strike_selection():
    """Process strike selection for all trading days."""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(os.path.dirname(current_dir), 'reports')
    
    # Read spot movement data
    try:
        spot_data = pd.read_csv(os.path.join(reports_dir, 'spot_movement.csv'))
        spot_data.set_index('date', inplace=True)
    except FileNotFoundError:
        print("Error: spot_movement.csv not found. Please run 02_get_spot_movement.py first.")
        return
    
    # Initialize results DataFrame
    results = pd.DataFrame(index=spot_data.index)
    
    # Process each day
    for date in spot_data.index:
        spot_price = spot_data.loc[date, 'price_1525']
        atm_strike, hedge_strike = select_strikes(spot_price)
        
        results.loc[date, 'spot_price'] = spot_price
        results.loc[date, 'atm_strike'] = atm_strike
        results.loc[date, 'hedge_strike'] = hedge_strike
        results.loc[date, 'direction'] = spot_data.loc[date, 'direction']
    
    # Save results
    results.to_csv(os.path.join(reports_dir, 'strike_selection.csv'))
    
    # Print summary
    print("\nStrike Selection Analysis:")
    print("=========================")
    print(f"Total days processed: {len(results)}")
    print("\nAverage Strikes by Direction:")
    print(results.groupby('direction')[['atm_strike', 'hedge_strike']].mean())
    print("\nSample of first 5 days:")
    print(results.head())
    
    return results

if __name__ == "__main__":
    process_strike_selection() 