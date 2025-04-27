import unittest
import sqlite3
from database import init_db, insert_expense
from datetime import datetime
import os

class TestFinanceTracker(unittest.TestCase):
    def setUp(self):
        """Set up a test database."""
        self.db_file = "test_finance.db"
        self.conn = sqlite3.connect(self.db_file)
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                category TEXT
            )
        """)
        self.conn.commit()

    def test_db_connection(self):
        """Test database creation and schema."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'")
        self.assertIsNotNone(cursor.fetchone())

    def test_insert_expense(self):
        """Test inserting an expense."""
        result = insert_expense("2025-04-20", 45.0, "Food")
        self.assertTrue(result)
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, amount, category FROM expenses")
        expense = cursor.fetchone()
        self.assertEqual(expense, ("2025-04-20", 45.0, "Food"))

    def tearDown(self):
        """Clean up test database."""
        self.conn.close()
        os.remove(self.db_file)

if __name__ == "__main__":
    unittest.main()