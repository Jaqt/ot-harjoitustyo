from entities.transaction import Transaction
from db import get_connection


class TransactionRepository:
    def create(self, transaction):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO transactions (user_id, year, month, transaction_type,
                category, amount, description) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (transaction.user_id, transaction.year, transaction.month,
                 transaction.transaction_type, transaction.category, transaction.amount,
                 transaction.description)
            )
            transaction.id = cursor.lastrowid
            return transaction

    def find_by_user_id(self, user_id):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT id, user_id, year, month, transaction_type, category,
                amount, description FROM transactions WHERE user_id = ?""",
                (user_id,)
            )
            rows = cursor.fetchall()

            return [
                Transaction(
                    id=row["id"],
                    user_id=row["user_id"],
                    year=row["year"],
                    month=row["month"],
                    transaction_type=row["transaction_type"],
                    category=row["category"],
                    amount=row["amount"],
                    description=row["description"]
                ) for row in rows
            ]

    def find_by_user_and_time(self, user_id, year, month):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT id, user_id, year, month, transaction_type, category,
                amount, description FROM transactions WHERE user_id = ? AND 
                year = ? AND month = ?""",
                (user_id, year, month)
            )
            rows = cursor.fetchall()

            return [
                Transaction(
                    id=row["id"],
                    user_id=row["user_id"],
                    year=row["year"],
                    month=row["month"],
                    transaction_type=row["transaction_type"],
                    category=row["category"],
                    amount=row["amount"],
                    description=row["description"]
                ) for row in rows
            ]

    def find_by_transaction_id(self, transaction_id):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT id, user_id, year, month, transaction_type, category,
                amount, description FROM transactions WHERE id = ?""",
                (transaction_id,)
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return Transaction(
                id=row["id"],
                user_id=row["user_id"],
                year=row["year"],
                month=row["month"],
                transaction_type=row["transaction_type"],
                category=row["category"],
                amount=row["amount"],
                description=row["description"]
            )

    def delete_all(self):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM transactions")
            connection.commit()
