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

    def test_find_by_transaction_id(self):
        transaction = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )

        match = self.transaction_repository.find_by_transaction_id(transaction.id)

        self.assertEqual(match.id, transaction.id)

    def test_find_by_invalid_transaction_id(self):
        transaction = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )

        match = self.transaction_repository.find_by_transaction_id(transaction.id + 1)

        self.assertIsNone(match)

    def test_update_transaction(self):
        transaction = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )

        transaction.amount = 1001
        self.transaction_repository.update(transaction)

        updated_transaction = self.transaction_repository.find_by_transaction_id(transaction.id)

        self.assertEqual(updated_transaction.amount, 1001)

    def test_find_by_user_id(self):
        transaction1 = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )
        transaction2 = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 5, "Menot", "Asuminen", 1000, "")
        )

        transactions = self.transaction_repository.find_by_user_id(self.user.id)

        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0].id, transaction1.id)
        self.assertEqual(transactions[1].id, transaction2.id)

    def test_find_by_user_id_with_no_transactions(self):
        transactions = self.transaction_repository.find_by_user_id(self.user.id)

        self.assertEqual(transactions, [])

    def test_find_by_user_and_time(self):
        transaction1 = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )
        transaction2 = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )
        transaction3 = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 5, "Menot", "Asuminen", 1000, "")
        )

        transactions1 = self.transaction_repository.find_by_user_and_time(self.user.id, 2026, 4)
        self.assertEqual(len(transactions1), 2)
        self.assertEqual(transactions1[0].id, transaction1.id)
        self.assertEqual(transactions1[1].id, transaction2.id)

        transactions2 = self.transaction_repository.find_by_user_and_time(self.user.id, 2026, 5)
        self.assertEqual(len(transactions2), 1)
        self.assertEqual(transactions2[0].id, transaction3.id)

    def test_find_by_user_and_time_with_no_transactions(self):
        transactions = self.transaction_repository.find_by_user_and_time(self.user.id, 2026, 4)

        self.assertEqual(transactions, [])

    def test_find_months_by_user_id(self):
        self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )
        self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )
        self.transaction_repository.create(
            Transaction(self.user.id, 2026, 5, "Menot", "Asuminen", 1000, "")
        )

        months = self.transaction_repository.find_months_by_user_id(self.user.id)

        self.assertEqual(len(months), 2)
        self.assertIn((2026, 4), months)
        self.assertIn((2026, 5), months)

    def test_find_months_by_user_id_with_no_transactions(self):
        months = self.transaction_repository.find_months_by_user_id(self.user.id)

        self.assertEqual(months, [])

    def test_delete_by_transaction_id(self):
        transaction = self.transaction_repository.create(
            Transaction(self.user.id, 2026, 4, "Menot", "Asuminen", 1000, "")
        )

        not_deleted = self.transaction_repository.find_by_transaction_id(transaction.id)
        self.assertIsNotNone(not_deleted)

        self.transaction_repository.delete_by_id(transaction.id)

        deleted_transaction = self.transaction_repository.find_by_transaction_id(transaction.id)
        self.assertIsNone(deleted_transaction)