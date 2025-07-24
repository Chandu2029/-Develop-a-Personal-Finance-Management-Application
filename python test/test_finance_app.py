import sqlite3
import os
from finance_app import init_db

def test_db_creation():
    if os.path.exists("finance_manager.db"):
        os.remove("finance_manager.db")
    init_db()
    assert os.path.exists("finance_manager.db"), "DB not created."
    print("Database creation test passed.")

if __name__ == "__main__":
    test_db_creation()
