# 📊 Personal Expense Tracker & Data Analytics System

A smart, modular, and dynamic **Personal Expense Tracker** developed in **Python** to streamline daily financial logging, enforce category budgets, and deliver comprehensive data insights. The application utilizes a secure relational database architecture paired with algorithmic analytical engines to provide real-time budget tracking and graphical financial visualizations.

---

## 🎓 Project Details
- **Project Name:** Personal Expense Tracker with Data Analytics and Visualization
- **Student Developer:** Yashik Jindal
- **Role & Configuration:** Database Design & Financial Data Engineering
- **Architecture Paradigm:** Modular Data-Centric Software System

---

## 🎯 Project Objectives
- **Eliminate Manual Logging:** Transition daily expense tracking from vulnerable sheets/registers to a robust relational system.
- **Budget Compliance:** Enforce real-time spending limits to immediately flag overspending categories.
- **Data Analytics Execution:** Implement computational algorithms to process structural historical expense metrics.
- **Visual Intelligence:** Convert raw financial rows into meaningful graphical insights for improved decision making.

---

## ✨ Features
- **📝 Structured Expense Logging:** Fast and dynamic entry mechanism to record expenditure amounts, dates, and explicit notes.
- **🏷️ Smart Category Management:** Supports precise sorting across financial divisions (e.g., Food, Travel, Entertainment, Utilities).
- **🛡️ Real-Time Budget Triggers:** Database-level budget checks that monitor expenditure ceilings and instantly issue warning flags if limits are breached.
- **📈 Advanced Data Analytics:** Mathematical evaluations mapping monthly trends, highest spending vectors, and averages.
- **📊 Graphical Visualizations:** Rich data representation using charts (Pie charts, Bar graphs) to visually map out category distributions.

---

## 🛠️ Project Structure & Component Purpose

| Component File | Operational Purpose |
| :--- | :--- |
| **`database.py`** | Creates the relational table structure, initializes connections, and handles raw SQL query logs. |
| **`expenses.py`** / **`app.py`** | The main core engine controlling structural program flows and user interaction endpoints. |
| **`analytics.py`** | Computational logic processing analytical data fields, financial calculations, and statistical sums. |
| **`visualizer.py`** | The graphics renderer using plotting modules to display chart models on the presentation layer. |
| **`expenses.db`** | The permanent local relational SQLite database housing user logs and schema rows. |

---

## 🗄️ Database Schema Design

### 1. `et_budgets` (Category Constraints)
- `category` (TEXT) - Primary Key tracking structural budget divisions (e.g., 'Food').
- `monthly_limit` (REAL) - Maximum allowed target expenditure capacity.
- `current_spent` (REAL) - Dynamic auto-incrementing field tracking cumulative category costs.

### 2. `et_expenses` (Transaction Logs)
- `expense_id` (INTEGER) - Primary Key driven by auto-incrementing identity logic.
- `category` (TEXT) - Foreign Key reference mapping connection properties to category nodes.
- `amount` (REAL) - Numeric data tracking exact cost parameters (Safe constraint checking `amount > 0`).
- `expense_date` (TEXT/DATE) - Clock timestamps recording transaction dates.

---

## 🚀 Local Installation & Execution

1. **Clone the Repo:** Download these repository assets onto your local workstation.
2. **Install Dependencies:** Open Command Prompt (CMD) in the root directory and install data plotting and visual design requirements:
   ```bash
   pip install matplotlib pandas
   ```
3. **Deploy the Application:** Launch the core script via python runner configurations:
   ```bash
   python app.py
   ```
4. **Data Analytics View:** To prompt computational reviews and display graphical metrics, run the dedicated visualization engine:
   ```bash
   python visualizer.py
   ```

---
*Developed for academic evaluation, modular python software engineering, and analytical financial programming paradigms.*
