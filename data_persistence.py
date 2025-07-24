import shutil
import os
import sqlite3

DB_NAME = "finance_manager.db"
BACKUP_NAME = "finance_manager_backup.db"

def backup_database():
    """Back up the current database file."""
    if not os.path.exists(DB_NAME):
        print("No database found to back up.")
        return

    shutil.copyfile(DB_NAME, BACKUP_NAME)
    print(f"Database backed up successfully to '{BACKUP_NAME}'.")

def restore_database():
    """Restore the database from the backup file."""
    if not os.path.exists(BACKUP_NAME):
        print("No backup found to restore.")
        return

    shutil.copyfile(BACKUP_NAME, DB_NAME)
    print(f"Database restored from '{BACKUP_NAME}'.")

def test_database_connection():
    """Test if the database connection works."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("SELECT 1")
        conn.close()
        print("Database connection test passed.")
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")

# Menu for stand-alone testing
def persistence_menu():
    while True:
        print("\n--- Data Persistence Menu ---")
        print("1. Backup Database")
        print("2. Restore Database")
        print("3. Test DB Connection")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            backup_database()
        elif choice == '2':
            restore_database()
        elif choice == '3':
            test_database_connection()
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    persistence_menu()
