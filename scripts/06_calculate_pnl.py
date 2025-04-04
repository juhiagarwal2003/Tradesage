import pandas as pd
import numpy as np
import os
from datetime import datetime

def calculate_pnl():
    """Calculate PnL and drawdown analysis from trailing exits."""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    reports_dir = os.path.join(base_dir, 'reports')
    
    # Read trailing exits data
    try:
        data = pd.read_csv(os.path.join(reports_dir, 'trailing_exits.csv'))
        data.set_index('date', inplace=True)
    except FileNotFoundError:
        print("Error: trailing_exits.csv not found. Please run 05_trailing_exit.py first.")
        return
    
    # Calculate P&L
    data['pnl'] = data.apply(
        lambda row: row['spot_points'] - row['option_premium'] if row['direction'] == 'UP' else row['spot_points'] - row['option_premium'],
        axis=1
    )
    
    # Calculate cumulative P&L
    data['cumulative_pnl'] = data['pnl'].cumsum()
    
    # Calculate drawdown
    data['peak'] = data['cumulative_pnl'].cummax()
    data['drawdown'] = data['cumulative_pnl'] - data['peak']
    
    # Calculate statistics
    stats = {
        'Total Trades': len(data),
        'Winning Trades': len(data[data['pnl'] > 0]),
        'Losing Trades': len(data[data['pnl'] < 0]),
        'Win Rate': len(data[data['pnl'] > 0]) / len(data) * 100,
        'Average Win': data[data['pnl'] > 0]['pnl'].mean(),
        'Average Loss': data[data['pnl'] < 0]['pnl'].mean(),
        'Largest Win': data['pnl'].max(),
        'Largest Loss': data['pnl'].min(),
        'Total P&L': data['pnl'].sum(),
        'Max Drawdown': data['drawdown'].min(),
        'Average Drawdown': data['drawdown'].mean()
    }
    
    # Calculate statistics by direction
    direction_stats = data.groupby('direction').agg({
        'pnl': ['count', 'mean', 'sum', 'min', 'max'],
        'spot_points': ['mean', 'sum'],
        'option_premium': ['mean', 'sum']
    })
    
    # Save results
    data.to_csv(os.path.join(reports_dir, 'pnl_analysis.csv'))
    
    # Print summary
    print("\nPnL and Drawdown Analysis:")
    print("=========================")
    print("\nOverall Statistics:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    
    print("\nStatistics by Direction:")
    print(direction_stats)
    
    print("\nSample of first 5 days:")
    print(data[['direction', 'spot_points', 'option_premium', 'pnl', 'cumulative_pnl', 'drawdown']].head())
    
    return data, stats, direction_stats

if __name__ == "__main__":
    calculate_pnl() 