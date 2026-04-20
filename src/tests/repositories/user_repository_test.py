import unittest

from entities.user import User
from repositories.user_repository import UserRepository

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        self.user_repository = UserRepository()
        self.user_repository.delete_all()

    def test_create_valid_user(self):
        user = self.user_repository.create(User("user", "password"))
        self.assertEqual(user.username, "user")
        self.assertEqual(user.password, "password")
