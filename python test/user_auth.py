import sqlite3
import getpass

DB_NAME = "finance_manager.db"

# Database Initialization
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
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
            login()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
