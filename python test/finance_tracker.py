import sqlite3

DB_NAME = "finance_manager.db"

def init_transaction_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL CHECK(amount >= 0),
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    
    conn.commit()
    conn.close()


def add_transaction(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    print("\n Adding New Transaction")
    t_type = input("Type (income/expense): ").strip().lower()
    if t_type not in ['income', 'expense']:
        print(" Invalid type.")
        return

    category = input("Category (e.g., Food, Rent, Salary): ")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print(" Invalid amount.")
        return
    
    date = input("Date (YYYY-MM-DD): ")

    c.execute('''
        INSERT INTO transactions (user_id, type, category, amount, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, t_type, category, amount, date))
    
    conn.commit()
    conn.close()
    print(" Transaction added successfully.")


def update_transaction(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    txn_id = input("Enter Transaction ID to update: ")
    c.execute("SELECT * FROM transactions WHERE id=? AND user_id=?", (txn_id, user_id))
    transaction = c.fetchone()

    if not transaction:
        print(" Transaction not found.")
        conn.close()
        return

    print(f"Current Data → Type: {transaction[2]}, Category: {transaction[3]}, Amount: {transaction[4]}, Date: {transaction[5]}")
    try:
        new_amount = float(input("New Amount: "))
    except ValueError:
        print(" Invalid amount.")
        return

    c.execute("UPDATE transactions SET amount=? WHERE id=?", (new_amount, txn_id))
    conn.commit()
    print(" Transaction updated.")
    conn.close()


def delete_transaction(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    txn_id = input("Enter Transaction ID to delete: ")
    c.execute("DELETE FROM transactions WHERE id=? AND user_id=?", (txn_id, user_id))
    conn.commit()
    if c.rowcount == 0:
        print(" No such transaction found.")
    else:
        print("  Transaction deleted.")
    conn.close()


def list_transactions(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    print("\n All Transactions")
    c.execute("SELECT id, type, category, amount, date FROM transactions WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if rows:
        print("{:<5} {:<10} {:<15} {:<10} {:<12}".format("ID", "Type", "Category", "Amount", "Date"))
        for r in rows:
            print("{:<5} {:<10} {:<15} {:<10} {:<12}".format(r[0], r[1], r[2], r[3], r[4]))
    else:
        print("No transactions found.")

    conn.close()

# Main interface for testing
def transaction_menu(user_id):
    init_transaction_table()

    while True:
        print("\n------ Transaction Menu (Days 6–10) ------")
        print("1. Add Transaction")
        print("2. Update Transaction")
        print("3. Delete Transaction")
        print("4. List All Transactions")
        print("5. Back to Main Menu")

        choice = input("Select an option: ")

        if choice == '1':
            add_transaction(user_id)
        elif choice == '2':
            update_transaction(user_id)
        elif choice == '3':
            delete_transaction(user_id)
        elif choice == '4':
            list_transactions(user_id)
        elif choice == '5':
            break
        else:
            print(" Invalid option. Please choose 1–5.")

# Example integration:
if __name__ == "__main__":
    user_id = input("Enter Dummy User ID to simulate logged in user: ")
    if user_id.isdigit():
        transaction_menu(int(user_id))
    else:
        print(" Invalid input. Use a numeric user ID.")
