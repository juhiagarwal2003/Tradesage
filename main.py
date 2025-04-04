import os
import sys
from datetime import datetime

def run_script(script_path):
    """Run a Python script and handle any errors."""
    script_name = os.path.basename(script_path)
    print(f"\nRunning {script_name}...")
    try:
        result = os.system(f"python {script_path}")
        return result == 0
    except Exception as e:
        print(f"Error running {script_name}: {str(e)}")
        return False

def main():
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    scripts_dir = os.path.join(current_dir, 'scripts')
    reports_dir = os.path.join(current_dir, 'reports')
    
    # Create reports directory if it doesn't exist
    os.makedirs(reports_dir, exist_ok=True)
    
    # List of scripts to run in order
    scripts = [
        "01_check_db.py",
        "02_get_spot_movement.py",
        "03_select_strike.py",
        "04_fetch_option_prices.py",
        "05_trailing_exit.py",
        "06_calculate_pnl.py",
        "07_generate_excel.py"
    ]
    
    # Run each script in sequence
    for script in scripts:
        script_path = os.path.join(scripts_dir, script)
        if not os.path.exists(script_path):
            print(f"Error: Script {script} not found at {script_path}")
            sys.exit(1)
            
        if not run_script(script_path):
            print(f"Stopping execution due to error in {script}")
            sys.exit(1)
    
    print("\nAll steps completed successfully!")
    print(f"Results saved in reports/Trade_Report.xlsx")

if __name__ == "__main__":
    main() 