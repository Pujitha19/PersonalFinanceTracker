import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv
import os
from datetime import datetime

class FinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.conn = sqlite3.connect("finance.db")
        self.create_db()
        self.setup_gui()

    def create_db(self):
        """Initialize SQLite database and expenses table."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                category TEXT
            )
        """)
        self.conn.commit()

    def setup_gui(self):
        """Set up the main GUI with tabs and entry form."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        # Tabs
        self.summary_frame = ttk.Frame(self.notebook)
        self.viz_frame = ttk.Frame(self.notebook)
        self.pred_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_frame, text="Expense Summary")
        self.notebook.add(self.viz_frame, text="Visualizations")
        self.notebook.add(self.pred_frame, text="Predictions")

        # Expense Entry Form
        entry_frame = ttk.LabelFrame(self.root, text="Add Expense")
        entry_frame.pack(pady=10, padx=10, fill="x")
        ttk.Label(entry_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5)
        self.date_entry = ttk.Entry(entry_frame)
        self.date_entry.grid(row=0, column=1, padx=5)
        ttk.Label(entry_frame, text="Amount:").grid(row=1, column=0, padx=5)
        self.amount_entry = ttk.Entry(entry_frame)
        self.amount_entry.grid(row=1, column=1, padx=5)
        ttk.Label(entry_frame, text="Category:").grid(row=2, column=0, padx=5)
        self.category_combo = ttk.Combobox(entry_frame, values=["Food", "Rent", "Entertainment", "Other"])
        self.category_combo.grid(row=2, column=1, padx=5)
        ttk.Button(entry_frame, text="Add Expense", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # Filter Panel
        filter_frame = ttk.LabelFrame(self.root, text="Filters")
        filter_frame.pack(pady=10, padx=10, fill="x")
        ttk.Label(filter_frame, text="Date Range:").grid(row=0, column=0, padx=5)
        self.date_range = ttk.Combobox(filter_frame, values=["Last 30 Days", "This Month", "All Time"])
        self.date_range.grid(row=0, column=1, padx=5)
        self.date_range.set("All Time")
        ttk.Label(filter_frame, text="Category:").grid(row=1, column=0, padx=5)
        self.filter_category = ttk.Combobox(filter_frame, values=["All", "Food", "Rent", "Entertainment", "Other"])
        self.filter_category.grid(row=1, column=1, padx=5)
        self.filter_category.set("All")
        ttk.Button(filter_frame, text="Apply Filter", command=self.update_summary).grid(row=2, column=0, columnspan=2, pady=10)

        # Export Button
        ttk.Button(self.root, text="Export Data", command=self.export_data).pack(pady=10)

        self.update_summary()
        self.setup_visualizations()

    def add_expense(self):
        """Validate and add expense to database."""
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_combo.get()

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Input", "Date must be in YYYY-MM-DD format.")
            return

        if not amount.replace(".", "", 1).isdigit() or float(amount) <= 0:
            messagebox.showerror("Invalid Input", "Amount must be a positive number.")
            return

        if not category:
            messagebox.showerror("Invalid Input", "Please select a category.")
            return

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO expenses (date, amount, category) VALUES (?, ?, ?)", (date, float(amount), category))
        self.conn.commit()
        messagebox.showinfo("Success", "Expense added successfully!")
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combo.set("")
        self.update_summary()
        self.setup_visualizations()

    def update_summary(self):
        """Update expense summary table based on filters."""
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        date_range = self.date_range.get()
        category = self.filter_category.get()

        query = "SELECT date, amount, category FROM expenses"
        conditions = []
        params = []

        if date_range == "Last 30 Days":
            conditions.append("date >= date('now', '-30 days')")
        elif date_range == "This Month":
            conditions.append("date LIKE ?")
            params.append(datetime.now().strftime("%Y-%m") + "%")

        if category != "All":
            conditions.append("category = ?")
            params.append(category)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        expenses = cursor.fetchall()

        tree = ttk.Treeview(self.summary_frame, columns=("Date", "Amount", "Category"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Amount", text="Amount")
        tree.heading("Category", text="Category")
        tree.pack(fill="both", expand=True)

        for expense in expenses:
            tree.insert("", tk.END, values=expense)

    def setup_visualizations(self):
        """Generate pie and bar charts in Visualizations tab."""
        for widget in self.viz_frame.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()
        if not data:
            return

        categories, amounts = zip(*data)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Pie Chart
        ax1.pie(amounts, labels=categories, autopct="%1.1f%%")
        ax1.set_title("Expense Breakdown by Category")

        # Bar Chart
        cursor.execute("SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses GROUP BY month")
        monthly_data = cursor.fetchall()
        if monthly_data:
            months, monthly_amounts = zip(*monthly_data)
            ax2.bar(months, monthly_amounts)
            ax2.set_title("Monthly Spending")
            ax2.set_xlabel("Month")
            ax2.set_ylabel("Amount")
            plt.setp(ax2.get_xticklabels(), rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
        plt.close(fig)

        self.setup_predictions()

    def setup_predictions(self):
        """Train linear regression model and display predictions."""
        for widget in self.pred_frame.winfo_children():
            widget.destroy()

        cursor = self.conn.cursor()
        cursor.execute("SELECT strftime('%Y-%m', date) AS month, SUM(amount) FROM expenses GROUP BY month")
        data = cursor.fetchall()
        if len(data) < 2:
            ttk.Label(self.pred_frame, text="Insufficient data for predictions.").pack()
            return

        months, amounts = zip(*data)
        X = np.arange(len(months)).reshape(-1, 1)
        y = np.array(amounts)

        model = LinearRegression()
        model.fit(X, y)
        future_X = np.arange(len(months), len(months) + 3).reshape(-1, 1)
        predictions = model.predict(future_X)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(range(len(months)), y, label="Historical")
        ax.plot(range(len(months), len(months) + 3), predictions, label="Predicted", linestyle="--")
        ax.set_xlabel("Month")
        ax.set_ylabel("Amount")
        ax.set_title("Expense Predictions (Next 3 Months)")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.pred_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Prediction Table
        tree = ttk.Treeview(self.pred_frame, columns=("Month", "Predicted Amount"), show="headings")
        tree.heading("Month", text="Month")
        tree.heading("Predicted Amount", text="Predicted Amount")
        tree.pack(fill="both", expand=True)

        for i, pred in enumerate(predictions, 1):
            tree.insert("", tk.END, values=(f"Month +{i}", f"${pred:.2f}"))

        plt.close(fig)

    def export_data(self):
        """Export expenses or predictions as CSV or PDF."""
        export_type = messagebox.askquestion("Export Type", "Export as CSV? (No for PDF)")
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, amount, category FROM expenses")
        expenses = cursor.fetchall()

        if export_type == "yes":
            with open("expenses.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Amount", "Category"])
                writer.writerows(expenses)
            messagebox.showinfo("Success", "Exported to expenses.csv")
        else:
            c = canvas.Canvas("expenses_report.pdf", pagesize=letter)
            c.drawString(100, 750, "Expense Report")
            y = 700
            for expense in expenses:
                c.drawString(100, y, f"{expense[0]}: ${expense[1]:.2f} ({expense[2]})")
                y -= 20
            c.save()
            messagebox.showinfo("Success", "Exported to expenses_report.pdf")

    def __del__(self):
        """Close database connection on exit."""
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceTrackerApp(root)
    root.mainloop()