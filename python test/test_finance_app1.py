import unittest
import os
import sqlite3
from .user_auth import init_db, register_user
from finance_tracker import init_transaction_table, add_transaction

DB_NAME = "finance_manager.db"

class TestFinanceApp(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
        init_db()
        init_transaction_table()
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        # Create a test user
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("testuser", "testpass"))
        self.conn.commit()
        self.user_id = self.cursor.lastrowid

    def test_user_creation(self):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", ("testuser",))
        user = self.cursor.fetchone()
        self.assertIsNotNone(user)

    def test_add_transaction(self):
        self.cursor.execute('''
            INSERT INTO transactions (user_id, type, category, amount, date)
            VALUES (?, ?, ?, ?, ?)''',
            (self.user_id, 'expense', 'Food', 100.0, '2025-07-21'))
        self.conn.commit()
        self.cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (self.user_id,))
        txn = self.cursor.fetchone()
        self.assertIsNotNone(txn)

    def tearDown(self):
        self.conn.close()
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)

if __name__ == '__main__':
    unittest.main()
