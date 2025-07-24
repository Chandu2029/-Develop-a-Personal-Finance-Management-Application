import sqlite3

DB_NAME = "finance_manager.db"

def init_budget_table():
    """Create the budgets table if it does not exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),
            month TEXT NOT NULL,
            UNIQUE(user_id, category, month),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def set_budget(user_id):
    """Enable user to set or update monthly budgets for categories."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    print("\nSet Monthly Budget")
    category = input("Enter category name (e.g., Food, Rent): ").strip()
    month = input("Enter month (YYYY-MM): ").strip()
    try:
        amount = float(input("Enter budget amount: "))
    except ValueError:
        print("Invalid amount. Must be a number.")
        conn.close()
        return

    # Insert or update budget for the user, category and month
    c.execute('''
        INSERT INTO budgets (user_id, category, amount, month) 
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, category, month) DO UPDATE SET amount=excluded.amount
    ''', (user_id, category, amount, month))
    conn.commit()
    conn.close()
    print(f"Budget set: {category} = {amount} for {month}")

def check_budget_exceeded(user_id, category, month):
    """
    Calculate total expenses for the user in the category and month,
    compare with budget, and notify if exceeded.
    """
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Get budget for that category and month
    c.execute('''
        SELECT amount FROM budgets
        WHERE user_id = ? AND category = ? AND month = ?
    ''', (user_id, category, month))
    budget_row = c.fetchone()
    if not budget_row:
        conn.close()
        return False  # No budget set, so cannot exceed

    budget_amount = budget_row[0]

    # Sum expenses for that category and month
    like_pattern = month + "%"
    c.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense' AND category = ? AND date LIKE ?
    ''', (user_id, category, like_pattern))
    total_expense = c.fetchone()[0] or 0.0

    conn.close()

    if total_expense > budget_amount:
        print(f"Alert: You have exceeded your budget for category '{category}'!")
        print(f"Spent: {total_expense} / Budget: {budget_amount}")
        return True
    return False

def list_budgets(user_id):
    """Display all budgets set by the user."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    print("\nYour Budgets:")
    c.execute('''
        SELECT category, amount, month FROM budgets
        WHERE user_id = ?
        ORDER BY month, category
    ''', (user_id,))
    rows = c.fetchall()
    if not rows:
        print("No budgets set yet.")
    else:
        for category, amount, month in rows:
            print(f"Category: {category}, Month: {month}, Budget: {amount}")
    conn.close()

# Example integration for testing or usage alongside other modules
def budget_menu(user_id):
    init_budget_table()
    while True:
        print("\n--- Budget Menu ---")
        print("1. Set/Update Budget")
        print("2. List Budgets")
        print("3. Check if Budget Exceeded for a Category and Month")
        print("4. Back to Main Menu")
        choice = input("Choose an option: ")

        if choice == '1':
            set_budget(user_id)
        elif choice == '2':
            list_budgets(user_id)
        elif choice == '3':
            category = input("Enter category to check: ").strip()
            month = input("Enter month (YYYY-MM): ").strip()
            check_budget_exceeded(user_id, category, month)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    user_input = input("Enter user ID: ")
    if user_input.isdigit():
        budget_menu(int(user_input))
    else:
        print("Invalid user ID.")
