import sqlite3

DB_NAME = "finance_manager.db"

def generate_report(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    print("\n--- Financial Report ---")
    period = input("Enter report period (YYYY or YYYY-MM): ").strip()

    # Validate input
    if len(period) not in [4, 7]:
        print("Invalid format. Use 'YYYY' or 'YYYY-MM'.")
        conn.close()
        return

    like_pattern = period + "%"
    
    # Total Income
    c.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'income' AND date LIKE ?
    ''', (user_id, like_pattern))
    total_income = c.fetchone()[0] or 0.0

    # Total Expense
    c.execute('''
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense' AND date LIKE ?
    ''', (user_id, like_pattern))
    total_expense = c.fetchone()[0] or 0.0

    savings = total_income - total_expense

    print(f"\nReport for period: {period}")
    print(f"Total Income   : {total_income:.2f}")
    print(f"Total Expenses : {total_expense:.2f}")
    print(f"Net Savings    : {savings:.2f}")

    # Category-wise expense breakdown
    print("\nExpenses by Category:")
    c.execute('''
        SELECT category, SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense' AND date LIKE ?
        GROUP BY category
    ''', (user_id, like_pattern))
    rows = c.fetchall()

    if rows:
        for category, total in rows:
            print(f"- {category}: {total:.2f}")
    else:
        print("No expenses found for this period.")

    conn.close()

# For testing/report menu
def report_menu(user_id):
    while True:
        print("1. Generate Income/Expense Report")
        print("2. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == '1':
            generate_report(user_id)
        elif choice == '2':
            break
        else:
            print("Invalid selection.")

# Standalone test
if __name__ == "__main__":
    user_id = input("Enter user ID: ")
    if user_id.isdigit():
        report_menu(int(user_id))
    else:
        print("Invalid user ID.")
