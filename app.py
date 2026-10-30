from analytics import predict_next_month_expense
from visualizer import generate_spending_charts

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

def handle_type_change(event):
    t_type = type_var.get()
    if t_type == "Income":
        cat_dropdown['values'] = ["Salary", "Business", "Freelance", "Investment", "Other Income"]
        cat_dropdown.set("Salary")
    else:
        cat_dropdown['values'] = ["Food", "Rent", "Bills", "Entertainment", "Travel", "Shopping", "Other Expense"]
        cat_dropdown.set("Food")

def add_transaction():
    t_type = type_var.get()
    category = cat_dropdown.get().strip()
    amount = amt_entry.get().strip()
    
    date_str = simpledialog.askstring("Transaction Date", "Enter date (YYYY-MM-DD):", initialvalue=datetime.now().strftime("%Y-%m-%d"))
    
    if not date_str:
        return

    if not category or not amount:
        messagebox.showerror("Error", "Please fill all the fields!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a valid number!")
        return

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)", 
                   (t_type, category, amount, date_str))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"{t_type} (${amount}) added under '{category}' successfully for date {date_str}!")
    amt_entry.delete(0, tk.END)
    update_dashboard()

def update_dashboard():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    res_inc = cursor.fetchone()
    total_income = res_inc[0] if res_inc and res_inc[0] is not None else 0.0
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    res_exp = cursor.fetchone()
    total_expense = res_exp[0] if res_exp and res_exp[0] is not None else 0.0
    
    balance = total_income - total_expense
    conn.close()

    inc_label.config(text=f"Total Income: ${total_income:.2f}", fg="green")
    exp_label.config(text=f"Total Expense: ${total_expense:.2f}", fg="red")
    bal_label.config(text=f"Net Balance: ${balance:.2f}", fg="blue" if balance >= 0 else "red")

def show_chart():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    res_inc = cursor.fetchone()
    total_income = res_inc[0] if res_inc and res_inc[0] is not None else 0.0
    
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data and total_income == 0:
        messagebox.showinfo("Info", "No data available to display chart!")
        return

    categories = [row[0] for row in data]
    amounts = [float(row[1]) for row in data]
    
    total_expense = sum(amounts)
    remaining_balance = total_income - total_expense

    if remaining_balance > 0:
        categories.append("Remaining Balance")
        amounts.append(remaining_balance)

    plt.figure(figsize=(6, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, 
            colors=['#ff9999','#6bbf75','#ffcc99','#66b3ff', '#c2c2f0', '#ffb3e6', '#3f51b5'])
    plt.title("Income Allocation & Expenses Breakdown")
    plt.show()

def clear_all_data():
    confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to delete all transactions?")
    if confirm:
        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions")
        conn.commit()
        conn.close()
        messagebox.showinfo("Reset Done", "All data has been cleared successfully!")
        update_dashboard()

def show_prediction():
    category = cat_dropdown.get().strip()
    result = predict_next_month_expense(category)
    if isinstance(result, str):
        messagebox.showinfo("Prediction Status", result)
    else:
        messagebox.showinfo("ML Prediction", f"Predicted expense for next month in {category}: Rs. {result}")

def show_dashboard():
    success = generate_spending_charts()
    if success:
        messagebox.showinfo("Success", "Analytics chart generated successfully inside 'static/' folder!")
    else:
        messagebox.showinfo("Error", "No expense data available to analyze.")

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("450x660")
root.config(bg="#f0f0f0")

tk.Label(root, text="💰 Expense Tracker 💰", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

tk.Label(frame, text="Type:", font=("Arial", 11), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
type_var = tk.StringVar(value="Expense")
type_dropdown = ttk.Combobox(frame, textvariable=type_var, values=["Income", "Expense"], state="readonly", width=18)
type_dropdown.grid(row=0, column=1, pady=5)
type_dropdown.bind("<<ComboboxSelected>>", handle_type_change)

tk.Label(frame, text="Category:", font=("Arial", 11), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
cat_dropdown = ttk.Combobox(frame, values=["Food", "Rent", "Bills", "Entertainment", "Travel", "Shopping", "Other Expense"], state="readonly", width=18)
cat_dropdown.grid(row=1, column=1, pady=5)
cat_dropdown.set("Food")

tk.Label(frame, text="Amount ($):", font=("Arial", 11), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
amt_entry = tk.Entry(frame, width=20, font=("Arial", 11))
amt_entry.grid(row=2, column=1, pady=5)

tk.Button(root, text="Add Transaction", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", width=20, command=add_transaction).pack(pady=10)

db_frame = tk.LabelFrame(root, text=" Dashboard ", font=("Arial", 12, "bold"), bg="#f0f0f0", bd=2, relief="groove")
db_frame.pack(pady=15, fill="x", padx=20)

inc_label = tk.Label(db_frame, text="Total Income: $0.00", font=("Arial", 11, "bold"), bg="#f0f0f0")
inc_label.pack(anchor="w", padx=10, pady=2)

exp_label = tk.Label(db_frame, text="Total Expense: $0.00", font=("Arial", 11, "bold"), bg="#f0f0f0")
exp_label.pack(anchor="w", padx=10, pady=2)

bal_label = tk.Label(db_frame, text="Net Balance: $0.00", font=("Arial", 12, "bold"), bg="#f0f0f0")
bal_label.pack(anchor="w", padx=10, pady=5)

tk.Button(root, text="📊 Show Expense Pie Chart", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", width=25, command=show_chart).pack(pady=5)
tk.Button(root, text="🔮 Predict Next Month Expense", font=("Arial", 11, "bold"), bg="#9C27B0", fg="white", width=25, command=show_prediction).pack(pady=5)
tk.Button(root, text="📈 Generate Analytics Dashboard", font=("Arial", 11, "bold"), bg="#FF9800", fg="white", width=25, command=show_dashboard).pack(pady=5)
tk.Button(root, text="🗑️ Clear All Data", font=("Arial", 11, "bold"), bg="#f44336", fg="white", width=25, command=clear_all_data).pack(pady=5)

update_dashboard()
root.mainloop()
