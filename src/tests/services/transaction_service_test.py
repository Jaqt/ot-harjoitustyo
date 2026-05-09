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

    def update(self, transaction):
        for index, existing_transaction in enumerate(self.transactions):
            if existing_transaction.id == transaction.id:
                self.transactions[index] = transaction
                return transaction

    def find_by_user_id(self, user_id):
        return [
            transaction for transaction in self.transactions
            if transaction.user_id == user_id
        ]

    def find_by_user_and_time(self, user_id, year, month):
        return [
            transaction for transaction in self.transactions
            if transaction.user_id == user_id
            and transaction.year == year
            and transaction.month == month
        ]

    def find_months_by_user_id(self, user_id):
        months = set()
        for transaction in self.transactions:
            if transaction.user_id == user_id:
                months.add((transaction.year, transaction.month))
        return sorted(months, reverse=True)

    def find_by_transaction_id(self, transaction_id):
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction
        return None

    def delete_by_id(self, transaction_id):
        self.transactions = [
            transaction for transaction in self.transactions
            if transaction.id != transaction_id
        ]

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

    def test_get_transactions_by_user_id_failure(self):
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

    def test_update_transaction(self):
        transaction = self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 1000, ""
        )

        updated_transaction = self.transaction_service.update_transaction(
            transaction.id, 2026, 4, "Menot", "Asuminen", 1001, ""
        )

        self.assertEqual(updated_transaction.amount, 1001)

    def test_update_transaction_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.update_transaction(
                1, 2026, 4, "Menot", "Asuminen", 1000, ""
            )

    def test_get_transactions_for_month(self):
        transaction1 = self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 1000, ""
        )
        transaction2 = self.transaction_service.add_transaction(
            2026, 4, "Menot", "Ruoka", 500, ""
        )
        transaction3 = self.transaction_service.add_transaction(
            2026, 5, "Menot", "Asuminen", 1000, ""
        )

        transactions1 = self.transaction_service.get_transactions_for_month(2026, 4)
        transactions2 = self.transaction_service.get_transactions_for_month(2026, 5)

        self.assertEqual(len(transactions1), 2)
        self.assertIn(transaction1, transactions1)
        self.assertIn(transaction2, transactions1)
        self.assertEqual(len(transactions2), 1)
        self.assertIn(transaction3, transactions2)

    def test_get_transactions_for_month_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.get_transactions_for_month(2026, 4)

    def test_get_transaction_months(self):
        self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 1000, ""
        )
        self.transaction_service.add_transaction(
            2026, 5, "Menot", "Asuminen", 1000, ""
        )

        months = self.transaction_service.get_transaction_months()

        self.assertEqual(len(months), 2)
        self.assertIn((2026, 4), months)
        self.assertIn((2026, 5), months)

    def test_get_transaction_months_with_no_transactions(self):
        months = self.transaction_service.get_transaction_months()

        self.assertEqual(months, [])

    def test_get_transaction_months_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.get_transaction_months()

    def test_delete_transaction(self):
        transaction = self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 1000, ""
        )

        self.transaction_service.delete_transaction(transaction.id)

        transactions = self.transaction_service.get_transactions_by_user_id(1)
        self.assertEqual(len(transactions), 0)

    def test_delete_transaction_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.delete_transaction(1)

    def test_delete_transaction_with_invalid_id(self):
        with self.assertRaises(TransactionNotFoundError):
            self.transaction_service.delete_transaction(123)

    def test_get_summary_for_month(self):
        self.transaction_service.add_transaction(
            2026, 4, "Tulot", "Palkka", 3000, ""
        )
        self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 1000, ""
        )
        self.transaction_service.add_transaction(
            2026, 4, "Menot", "Ruoka", 500, ""
        )

        total_income, total_expense = self.transaction_service.get_summary_for_month(2026, 4)

        self.assertEqual(total_income, 3000)
        self.assertEqual(total_expense, 1500)

    def test_get_summary_for_month_with_no_transactions(self):
        total_income, total_expense = self.transaction_service.get_summary_for_month(2026, 4)

        self.assertEqual(total_income, 0)
        self.assertEqual(total_expense, 0)

    def test_get_csv_data_for_month(self):
        self.transaction_service.add_transaction(
            2026, 4, "Tulot", "Palkka", 3000, ""
        )
        self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 1000, ""
        )

        header, rows = self.transaction_service.get_csv_export_data_for_month(2026, 4)

        self.assertEqual(len(rows), 2)
        self.assertIn([2026, 4, "Tulot", "Palkka", 3000, ""], rows)
        self.assertIn([2026, 4, "Menot", "Asuminen", 1000, ""], rows)

    def test_get_csv_data_for_month_with_no_transactions(self):
        header, rows = self.transaction_service.get_csv_export_data_for_month(2026, 4)

        self.assertEqual(rows, [])

    def test_get_csv_data_for_month_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.get_csv_export_data_for_month(2026, 4)

    def test_get_category_distribution_for_month(self):
        self.transaction_service.add_transaction(
            2026, 4, "Menot", "Asuminen", 1000, ""
        )
        self.transaction_service.add_transaction(
            2026, 4, "Menot", "Ruoka", 500, ""
        )

        labels, values = self.transaction_service.get_category_distribution_for_month(2026, 4, "Menot")

        result = dict(zip(labels, values))
        self.assertEqual(result["Asuminen"], 1000)
        self.assertEqual(result["Ruoka"], 500)

    def test_get_category_distribution_for_month_with_no_transactions(self):
        labels, values = self.transaction_service.get_category_distribution_for_month(2026, 4, "Menot")

        self.assertEqual(labels, [])
        self.assertEqual(values, [])

    def test_get_category_distribution_for_month_without_user_raises_error(self):
        transaction_service = TransactionService(
            FakeTransactionRepository(), FakeUserService(None))

        with self.assertRaises(UserNotLoggedInError):
            transaction_service.get_category_distribution_for_month(2026, 4, "Menot")
