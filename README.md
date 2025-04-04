# TradeSage: Intelligent Trading Strategy Analysis

![TradeSage Logo](https://via.placeholder.com/150)  *(Add your logo here)*

TradeSage is an intelligent trading strategy analysis system that combines sophisticated data processing with smart trading insights. It's designed to analyze options trading strategies with precision and generate comprehensive performance reports.

## 🌟 Features

- **Smart Database Analysis**: Intelligent exploration of market data structures
- **Precision Strike Selection**: Advanced algorithms for ATM and hedge strike selection
- **Adaptive Trailing Stops**: Dynamic 3-minute trailing stop implementation
- **Comprehensive Analytics**: Detailed PnL and drawdown analysis
- **Professional Reporting**: Automated Excel report generation

## 📁 Project Structure

```
TradeSage/
├── data/               # Market data storage
│   ├── SPOT.db        # Spot price database
│   └── OPT.db         # Options database
├── scripts/           # Analysis modules
│   ├── 01_check_db.py
│   ├── 02_get_spot_movement.py
│   ├── 03_select_strike.py
│   ├── 04_fetch_option_prices.py
│   ├── 05_trailing_exit.py
│   ├── 06_calculate_pnl.py
│   └── 07_generate_excel.py
├── reports/           # Analysis outputs
│   └── Trade_Report.xlsx
├── requirements.txt   # Dependencies
└── README.md         # Documentation
```

## 🚀 Quick Start

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/tradesage.git
   cd tradesage
   ```

2. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run Analysis**
   ```bash
   python scripts/01_check_db.py
   # ... run other scripts in sequence
   python scripts/07_generate_excel.py
   ```

## 📊 Analysis Pipeline

1. **Database Exploration** (`01_check_db.py`)
   - Analyze database structure
   - Validate data integrity

2. **Market Analysis** (`02_get_spot_movement.py`)
   - Calculate price movements
   - Identify market trends

3. **Strategy Setup** (`03_select_strike.py`, `04_fetch_option_prices.py`)
   - Select optimal strikes
   - Calculate option premiums

4. **Trade Execution** (`05_trailing_exit.py`)
   - Implement trailing stops
   - Track exit points

5. **Performance Analysis** (`06_calculate_pnl.py`)
   - Calculate P&L
   - Analyze drawdowns

6. **Report Generation** (`07_generate_excel.py`)
   - Generate comprehensive reports
   - Export analysis results

## 📈 Key Metrics

- Trade success rate
- Average profit/loss
- Maximum drawdown
- Risk-adjusted returns
- Direction-wise performance

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python
- Powered by pandas and numpy
- Inspired by quantitative trading strategies

---

*TradeSage - Your Intelligent Trading Companion* 