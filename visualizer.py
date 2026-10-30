import sqlite3
import os
import matplotlib.pyplot as plt

def generate_spending_charts():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    query = "SELECT category, SUM(amount) FROM transactions WHERE type = 'Expense' GROUP BY category"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        return False
        
    categories = [row[0] for row in data]
    amounts = [float(row[1]) for row in data]
    
    plt.figure(figsize=(8, 6))
    colors = ['#ff9999','#6bbf75','#66b3ff','#99ff99','#ffcc99','#c2c2f0']
    
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140, colors=colors, 
            wedgeprops={'edgecolor': 'black', 'linewidth': 1, 'antialiased': True})
    
    plt.title('Category-wise Expense Distribution (Data Analytics)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    if not os.path.exists('static'):
        os.makedirs('static')
        
    plt.savefig('static/spending_chart.png', dpi=300)
    plt.close()
    return True
