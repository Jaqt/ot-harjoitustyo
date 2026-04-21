import unittest

from entities.user import User
from repositories.user_repository import UserRepository
from repositories.transaction_repository import TransactionRepository


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()
        self.transaction_repository = TransactionRepository()

        self.transaction_repository.delete_all()
        self.user_repository.delete_all()

    def test_create_valid_user(self):
        user = self.user_repository.create(User("user", "password"))

        self.assertEqual(user.username, "user")
        self.assertEqual(user.password, "password")

    def test_find_by_username_valid(self):
        user = self.user_repository.create(User("user", "password"))

        self.assertEqual(self.user_repository.find_by_username("user").username, "user")
        self.assertEqual(self.user_repository.find_by_username("user").password, "password")
        self.assertEqual(self.user_repository.find_by_username("user").id, user.id)

    def test_find_by_username_invalid(self):
        self.user_repository.create(User("user", "password"))

        self.assertIsNone(self.user_repository.find_by_username("invalid"))
