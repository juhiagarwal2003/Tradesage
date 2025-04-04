import sqlite3
import pandas as pd
import os

def explore_database(db_path):
    """Explore the structure of a SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nTables in {db_path}:")
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        
        # Get column information
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns = cursor.fetchall()
        print("Columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Get sample data
        cursor.execute(f"SELECT * FROM '{table_name}' LIMIT 1;")
        sample_data = cursor.fetchall()
        if sample_data:
            print("\nSample data:")
            df = pd.DataFrame(sample_data, columns=[col[1] for col in columns])
            print(df)
            print("\nUnique values in each column:")
            for col in df.columns:
                cursor.execute(f"SELECT DISTINCT {col} FROM '{table_name}' LIMIT 5;")
                unique_vals = cursor.fetchall()
                print(f"  {col}: {[val[0] for val in unique_vals]}")
    
    conn.close()

def check_database_structure():
    """Check the structure of both databases and print details."""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    data_dir = os.path.join(base_dir, 'data')
    
    # Check SPOT database
    print("\nChecking SPOT database structure:")
    print("================================")
    spot_conn = sqlite3.connect(os.path.join(data_dir, 'SPOT.db'))
    spot_cursor = spot_conn.cursor()
    
    # Get all table names
    spot_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = spot_cursor.fetchall()
    print(f"\nFound {len(tables)} tables in SPOT database:")
    for table in tables[:5]:  # Show first 5 tables
        print(f"- {table[0]}")
    
    if tables:
        # Get sample data from first table
        first_table = tables[0][0]
        print(f"\nSample data from table '{first_table}':")
        spot_cursor.execute(f"SELECT * FROM '{first_table}' LIMIT 1")
        columns = [description[0] for description in spot_cursor.description]
        print("Columns:", columns)
        
        # Get time range for first table
        spot_cursor.execute(f"""
            SELECT MIN(time), MAX(time)
            FROM '{first_table}'
            WHERE time >= '09:15:00' AND time <= '15:30:00'
        """)
        min_time, max_time = spot_cursor.fetchone()
        print(f"Time range: {min_time} to {max_time}")
    
    spot_conn.close()

if __name__ == "__main__":
    check_database_structure()
    
    # Explore spot price database
    print("Exploring SPOT database...")
    explore_database(os.path.join(data_dir, 'SPOT.db'))
    
    # Explore options database
    print("\nExploring OPT database...")
    explore_database(os.path.join(data_dir, 'OPT.db')) 