# Personal Finance Tracker with Predictive Insights

## Overview
A desktop application to track expenses, visualize spending, and predict future expenses using machine learning.

## Requirements
- Python 3.11
- Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- 2 GB RAM, 100 MB free disk space

## Installation
1. Clone the repository: `git clone [your-repo-url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python main.py`

## Usage
- **Add Expenses**: Enter date (YYYY-MM-DD), amount, and category.
- **View Summary**: Filter by date range or category.
- **Visualizations**: See pie and bar charts in the Visualizations tab.
- **Predictions**: View 3-month expense predictions in the Predictions tab.
- **Export**: Save data as CSV or PDF.

## Troubleshooting
- **App won’t start**: Ensure Python 3.11 and dependencies are installed.
- **No predictions**: Add at least 2 months of expense data.
- **GUI issues**: Check screen resolution (min 1024x768).

## Running Tests
```bash
python -m unittest test_main.py