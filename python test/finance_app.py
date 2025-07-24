import sqlite3
import getpass

DB_NAME = "finance_manager.db"

# Database Initialization
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )''')
    # Transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        category TEXT,
        amount REAL,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    # Budgets table
    c.execute('''CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        category TEXT,
        amount REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

# User Registration
def register():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("\n--- User Registration ---")
    username = input("Enter a new username: ")
    password = getpass.getpass("Enter a new password: ")
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

# User Login
def login():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("\n--- User Login ---")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    if result:
        print("Login successful.")
        conn.close()
        return result[0]
    
    else:
        print("Invalid credentials.")
        conn.close()
        return None

# Add Transaction
def add_transaction(user_id, t_type):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print(f"\n--- Add {t_type.title()} ---")
    category = input("Category: ")
    try:
        amount = float(input("Amount: "))
        date = input("Date (YYYY-MM-DD): ")
        c.execute("INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
                  (user_id, t_type, category, amount, date))
        conn.commit()
        print(f"{t_type.title()} added successfully.")
        if t_type == "expense":
            # Check if budget is exceeded
            c.execute('''SELECT amount FROM budgets WHERE user_id=? AND category=?''', (user_id, category))
            budget = c.fetchone()
            if budget:
                c.execute('''SELECT SUM(amount) FROM transactions WHERE user_id=? AND type='expense' AND category=?''', (user_id, category))
                spent = c.fetchone()[0]
                if spent > budget[0]:
                    print(f"Alert: Budget exceeded for category '{category}'.")
    except ValueError:
        print("Invalid amount.")
    conn.close()

# Update Transaction
def update_transaction(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("\n--- Update Transaction ---")
    txn_id = input("Enter transaction ID to update: ")
    c.execute("SELECT * FROM transactions WHERE id=? AND user_id=?", (txn_id, user_id))
    txn = c.fetchone()
    if not txn:
        print("Transaction not found.")
        conn.close()
        return
    new_amount = float(input("New Amount: "))
    c.execute("UPDATE transactions SET amount=? WHERE id=?", (new_amount, txn_id))
    conn.commit()
    print("Transaction updated.")
    conn.close()

# Delete Transaction
def delete_transaction(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("\n--- Delete Transaction ---")
    txn_id = input("Enter transaction ID to delete: ")
    c.execute("DELETE FROM transactions WHERE id=? AND user_id=?", (txn_id, user_id))
    conn.commit()
    print("Transaction deleted (if existed).")
    conn.close()

# Set Budget
def set_budget(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("\n--- Set Monthly Budget ---")
    category = input("Category: ")
    try:
        amount = float(input("Budget amount: "))
        c.execute("INSERT OR REPLACE INTO budgets (user_id, category, amount) VALUES (?, ?, ?)", (user_id, category, amount))
        conn.commit()
        print("Budget set/updated.")
    except ValueError:
        print("Invalid amount.")
    conn.close()

# Generate Reports
def financial_report(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("\n--- Financial Report ---")
    period = input("Report period (YYYY-MM or YYYY): ")
    # Monthly report
    if len(period) == 7:
        like_pattern = period + "%"
    else:
        like_pattern = period + "%"

    c.execute('''SELECT SUM(amount) FROM transactions
                 WHERE user_id=? AND type='income' AND date LIKE ?''', (user_id, like_pattern))
    total_income = c.fetchone()[0] or 0.0

    c.execute('''SELECT SUM(amount) FROM transactions
                 WHERE user_id=? AND type='expense' AND date LIKE ?''', (user_id, like_pattern))
    total_expense = c.fetchone()[0] or 0.0

    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Savings: {total_income - total_expense}")

    # Show category-wise expenses for this period
    c.execute('''SELECT category, SUM(amount) FROM transactions
                 WHERE user_id=? AND type='expense' AND date LIKE ?
                 GROUP BY category''', (user_id, like_pattern))
    rows = c.fetchall()
    if rows:
        print("Expenses by Category:")
        for category, amount in rows:
            print(f"  {category}: {amount}")
    conn.close()

# Backup Data
def backup_data():
    import shutil
    shutil.copy(DB_NAME, DB_NAME + ".bak")
    print("Database backup created.")

# Restore Data
def restore_data():
    import shutil
    shutil.copy(DB_NAME + ".bak", DB_NAME)
    print("Database restored from backup.")

# List Transactions for User
def list_transactions(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("\n--- All Transactions ---")
    c.execute("SELECT id, type, category, amount, date FROM transactions WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    if rows:
        print("{:<5}{:<10}{:<15}{:<10}{:<12}".format("ID", "Type", "Category", "Amount", "Date"))
        for r in rows:
            print("{:<5}{:<10}{:<15}{:<10}{:<12}".format(*r))
    else:
        print("No transactions found.")
    conn.close()

# Main Menu
def main():
    init_db()
    print("Welcome to Personal Finance Manager")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
            if user_id:
                user_menu(user_id)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

def user_menu(user_id):
    while True:
        print("""
1. Add Income
2. Add Expense
3. Update Transaction
4. Delete Transaction
5. Set Monthly Budget
6. Financial Report
7. List All Transactions
8. Backup Data
9. Restore Data
10. Logout
        """)
        choice = input("Choose operation: ")
        if choice == '1':
            add_transaction(user_id, "income")
        elif choice == '2':
            add_transaction(user_id, "expense")
        elif choice == '3':
            update_transaction(user_id)
        elif choice == '4':
            delete_transaction(user_id)
        elif choice == '5':
            set_budget(user_id)
        elif choice == '6':
            financial_report(user_id)
        elif choice == '7':
            list_transactions(user_id)
        elif choice == '8':
            backup_data()
        elif choice == '9':
            restore_data()
        elif choice == '10':
            print("Logging out...")
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
