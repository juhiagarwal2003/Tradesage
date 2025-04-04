import sqlite3
import pandas as pd
from datetime import datetime, time
import os

def get_spot_movement():
    """Analyze spot price movement between 9:15 AM and 3:25 PM."""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    reports_dir = os.path.join(os.path.dirname(current_dir), 'reports')
    
    # Create reports directory if it doesn't exist
    os.makedirs(reports_dir, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(os.path.join(data_dir, 'SPOT.db'))
    cursor = conn.cursor()
    
    # Get all tables (dates)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    dates = [table[0] for table in cursor.fetchall()]
    
    # Initialize results DataFrame
    results = []
    
    # Process each date
    for date in dates:
        try:
            # Query for 9:15 AM price
            cursor.execute(f"""
                SELECT time, close as price
                FROM "{date}"
                WHERE time = '09:15:00'
            """)
            morning_data = cursor.fetchone()
            
            # Query for 3:25 PM price
            cursor.execute(f"""
                SELECT time, close as price
                FROM "{date}"
                WHERE time = '15:25:00'
            """)
            afternoon_data = cursor.fetchone()
            
            if morning_data and afternoon_data:
                results.append({
                    'date': date,
                    'price_915': morning_data[1],
                    'price_1525': afternoon_data[1]
                })
        except sqlite3.OperationalError as e:
            print(f"Error processing date {date}: {str(e)}")
            continue
    
    conn.close()
    
    # Convert results to DataFrame
    df_pivot = pd.DataFrame(results)
    if not df_pivot.empty:
        df_pivot.set_index('date', inplace=True)
        
        # Calculate price movement
        df_pivot['price_change'] = df_pivot['price_1525'] - df_pivot['price_915']
        df_pivot['direction'] = df_pivot['price_change'].apply(
            lambda x: 'UP' if x > 0 else 'DOWN' if x < 0 else 'FLAT'
        )
        
        # Calculate percentage change
        df_pivot['pct_change'] = (df_pivot['price_change'] / df_pivot['price_915'] * 100).round(2)
        
        # Save results
        df_pivot.to_csv(os.path.join(reports_dir, 'spot_movement.csv'))
        
        # Print summary
        print("\nSpot Price Movement Analysis:")
        print("=============================")
        print(f"Total trading days analyzed: {len(df_pivot)}")
        print("\nDirection Summary:")
        print(df_pivot['direction'].value_counts())
        print("\nAverage Price Change: {:.2f}%".format(df_pivot['pct_change'].mean()))
        print("\nSample of first 5 days:")
        print(df_pivot.head())
        
        return df_pivot
    else:
        print("No data found for analysis")
        return None

if __name__ == "__main__":
    get_spot_movement() 