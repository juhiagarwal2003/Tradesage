import pandas as pd
import os
from datetime import datetime

def generate_excel_report():
    """Generate a comprehensive Excel report with all analysis results."""
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)
    reports_dir = os.path.join(base_dir, 'reports')
    
    # Check for required files
    required_files = [
        'spot_movement.csv',
        'strike_selection.csv',
        'option_prices.csv',
        'trailing_exits.csv',
        'pnl_analysis.csv'
    ]
    
    for file in required_files:
        if not os.path.exists(os.path.join(reports_dir, file)):
            print(f"Error: {file} not found. Please run all previous scripts first.")
            return
    
    # Create Excel writer
    excel_file = os.path.join(reports_dir, 'Trade_Report.xlsx')
    writer = pd.ExcelWriter(excel_file, engine='openpyxl')
    
    # Read and format each dataset
    spot_movement = pd.read_csv(os.path.join(reports_dir, 'spot_movement.csv'))
    strike_selection = pd.read_csv(os.path.join(reports_dir, 'strike_selection.csv'))
    option_prices = pd.read_csv(os.path.join(reports_dir, 'option_prices.csv'))
    trailing_exits = pd.read_csv(os.path.join(reports_dir, 'trailing_exits.csv'))
    pnl_analysis = pd.read_csv(os.path.join(reports_dir, 'pnl_analysis.csv'))
    
    # Write each dataset to a separate sheet
    spot_movement.to_excel(writer, sheet_name='Spot Movement', index=False)
    strike_selection.to_excel(writer, sheet_name='Strike Selection', index=False)
    option_prices.to_excel(writer, sheet_name='Option Prices', index=False)
    trailing_exits.to_excel(writer, sheet_name='Trailing Exits', index=False)
    pnl_analysis.to_excel(writer, sheet_name='PnL Analysis', index=False)
    
    # Create summary sheet
    summary_data = {
        'Metric': [
            'Total Trading Days',
            'Total Trades',
            'Winning Trades',
            'Losing Trades',
            'Win Rate',
            'Average Win',
            'Average Loss',
            'Largest Win',
            'Largest Loss',
            'Total P&L',
            'Max Drawdown',
            'Average Drawdown'
        ],
        'Value': [
            len(spot_movement),
            len(trailing_exits),
            len(pnl_analysis[pnl_analysis['pnl'] > 0]),
            len(pnl_analysis[pnl_analysis['pnl'] < 0]),
            len(pnl_analysis[pnl_analysis['pnl'] > 0]) / len(pnl_analysis) * 100,
            pnl_analysis[pnl_analysis['pnl'] > 0]['pnl'].mean(),
            pnl_analysis[pnl_analysis['pnl'] < 0]['pnl'].mean(),
            pnl_analysis['pnl'].max(),
            pnl_analysis['pnl'].min(),
            pnl_analysis['pnl'].sum(),
            pnl_analysis['drawdown'].min(),
            pnl_analysis['drawdown'].mean()
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    # Create direction-wise summary
    direction_summary = pnl_analysis.groupby('direction').agg({
        'pnl': ['count', 'mean', 'sum', 'min', 'max'],
        'spot_points': ['mean', 'sum'],
        'option_premium': ['mean', 'sum']
    }).round(2)
    
    direction_summary.to_excel(writer, sheet_name='Direction Summary')
    
    # Save the Excel file
    writer.close()
    
    print(f"\nExcel report generated successfully: {excel_file}")
    print("\nReport Contents:")
    print("1. Summary - Key performance metrics")
    print("2. Direction Summary - Performance by trade direction")
    print("3. Spot Movement - Daily spot price movements")
    print("4. Strike Selection - Selected strike prices")
    print("5. Option Prices - Option premiums")
    print("6. Trailing Exits - Exit points and times")
    print("7. PnL Analysis - Detailed P&L and drawdown analysis")

if __name__ == "__main__":
    generate_excel_report() 