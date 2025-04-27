
## Instructions to Run, Test, and Package

### Prerequisites
- **Python 3.11**: Download from [python.org](https://www.python.org/downloads/).
- **IDE**: Visual Studio Code (recommended).
- **Git**: For version control (optional).
- **OS**: Windows (for `.exe`; macOS/Linux instructions provided separately).

### Setup
1. **Create Project Directory**:
   - Create a folder (e.g., `PersonalFinanceTracker`).
   - Save the above files (`main.py`, `database.py`, `test_main.py`, `requirements.txt`, `README.md`) in this folder.
2. **Install Dependencies**:
   - Open a terminal in the project directory.
   - Run: `pip install -r requirements.txt`
3. **Run the Application**:
   - Run: `python main.py`
   - The GUI should launch, allowing you to add expenses, view summaries, and see predictions.
4. **Run Unit Tests**:
   - Run: `python -m unittest test_main.py`
   - Tests should pass, confirming database and insert functionality.

### Generating the `.exe` (Windows)
1. **Install PyInstaller**:
   - Run: `pip install pyinstaller`
2. **Package the Application**:
   - In the terminal, navigate to the project directory.
   - Run: `pyinstaller --onefile --windowed main.py`
   - This creates a single `.exe` file in the `dist` folder (e.g., `dist/main.exe`).
3. **Test the Executable**:
   - Double-click `dist/main.exe` to launch the app.
   - Ensure all features (expense entry, visualizations, export) work.
4. **Distribute**:
   - Copy `main.exe` to any Windows machine with compatible specs (Windows 10/11, 2 GB RAM).
   - The SQLite database (`finance.db`) will be created in the same directory as the `.exe`.

### For macOS/Linux
- **macOS**: Use `pyinstaller --onefile --windowed main.py` to create a `.app` bundle or single executable. Run the output in `dist/`.
- **Linux**: Same command, but ensure Tkinter is installed (`sudo apt-get install python3-tk` on Ubuntu). The output is a binary in `dist/`.
- Note: These won’t produce a `.exe` but a platform-specific executable. Let me know if you need a macOS/Linux-specific guide.

### Troubleshooting
- **PyInstaller Errors**: Ensure all dependencies are installed and Python 3.11 is used. Check for missing modules with `pip list`.
- **GUI Not Displaying**: Verify Tkinter is installed (`python -m tkinter` should open a test window).
- **Predictions Fail**: Add at least two months of expense data (e.g., “2025-03-01, 100, Food” and “2025-04-01, 150, Rent”).
- **Export Issues**: Ensure write permissions in the output directory and `reportlab` is installed.
