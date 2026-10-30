import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

def predict_next_month_expense(category):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    
    query = "SELECT date, amount FROM transactions WHERE category = ? AND type = 'Expense'"
    cursor.execute(query, (category,))
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        return "Insufficient data for prediction (No records found)"
        
    monthly_data = {}
    for row in data:
        date_str = str(row[0])
        amount = float(row[1])
        try:
            year_month = date_str[:7]
            monthly_data[year_month] = monthly_data.get(year_month, 0.0) + amount
        except Exception:
            continue
            
    sorted_months = sorted(monthly_data.keys())
    
    if len(sorted_months) < 2:
        return f"Insufficient data for prediction (Need at least 2 different months. Current unique months: {len(sorted_months)})"
        
    X = np.array(range(len(sorted_months))).reshape(-1, 1)
    y = np.array([monthly_data[m] for m in sorted_months])
    
    model = LinearRegression()
    model.fit(X, y)
    
    next_month_step = np.array([[len(sorted_months)]])
    predicted_amount = model.predict(next_month_step)
    
    # यहाँ .item() जोड़कर एरे से वैल्यू को बाहर निकाला गया है ताकि scalar एरर न आए
    val = float(predicted_amount.item())
    
    return round(max(0.0, val), 2)
