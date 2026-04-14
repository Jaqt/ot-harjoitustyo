import unittest

from entities.user import User
from services.transaction_service import (
    TransactionService,
    TransactionNotFoundError,
    UserNotLoggedInError
)


class FakeTransactionRepository:
    def __init__(self, transactions=None):
        self.transactions = transactions or []

    def create(self, transaction):
        transaction.id = len(self.transactions) + 1
        self.transactions.append(transaction)
        return transaction

    def find_by_user_id(self, user_id):
        return [row for row in self.transactions if row.user_id == user_id]

    def find_by_transaction_id(self, transaction_id):
        for row in self.transactions:
            if row.id == transaction_id:
                return row
        return None

class FakeUserService:
    def __init__(self, user=None):
        self._user = user

    def get_current_user(self):
        return self._user

class TestTransactionService(unittest.TestCase):
    def setUp(self):
        self.valid_user = User("user", "password", 1)
        self.transaction_service = TransactionService(
            FakeTransactionRepository(),
            FakeUserService(self.valid_user)
        )

    def test_add_valid_transaction(self):
        transaction = self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 100.0, ""
        )

        self.assertEqual(transaction.user_id, 1)
        self.assertEqual(transaction.year, 2026)
        self.assertEqual(transaction.month, 4)
        self.assertEqual(transaction.transaction_type, "Menot")
        self.assertEqual(transaction.category, "Asuminen")
        self.assertEqual(transaction.amount, 100.0)
        self.assertEqual(transaction.description, "")

    def test_add_transaction_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.add_transaction(
                2026, 4, "Menot", "Asuminen", 100.0, ""
            )

    def test_get_transactions_by_user_id_success(self):
        transaction = self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 100.0, ""
        )

        transactions = self.transaction_service.get_transactions_by_user_id(1)
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0], transaction)

    def test_get_transactions_by_user_id_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.get_transactions_by_user_id(1)

    def test_get_transaction_by_user_id_failure(self):
        with self.assertRaises(TransactionNotFoundError):
            self.transaction_service.get_transactions_by_user_id(123)

    def test_get_transaction_by_transaction_id_success(self):
        transaction = self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 100.0, ""
        )

        return_transaction = self.transaction_service.get_transaction_by_transaction_id(transaction.id)
        self.assertEqual(return_transaction, transaction)

    def test_get_transaction_by_transaction_id_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.get_transaction_by_transaction_id(1)

    def test_get_transaction_by_transaction_id_failure(self):
        with self.assertRaises(TransactionNotFoundError):
            self.transaction_service.get_transaction_by_transaction_id(123)
