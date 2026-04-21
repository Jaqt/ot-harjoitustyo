import unittest

from entities.transaction import Transaction
from entities.user import User
from repositories.user_repository import UserRepository
from repositories.transaction_repository import TransactionRepository


class TestTransactionRepository(unittest.TestCase):
    def setUp(self):
        self.transaction_repository = TransactionRepository()
        self.user_repository = UserRepository()

        self.transaction_repository.delete_all()
        self.user_repository.delete_all()

        self.user = self.user_repository.create(User("user", "password"))

    def test_create_valid_transaction(self):
        transaction = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )

        self.assertEqual(transaction.user_id, self.user.id)
        self.assertEqual(transaction.year, 2026)
        self.assertEqual(transaction.month, 4)
        self.assertEqual(transaction.transaction_type, "Menot")
        self.assertEqual(transaction.category, "Asuminen")
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.description, "")
        self.assertIsNotNone(transaction.id)
