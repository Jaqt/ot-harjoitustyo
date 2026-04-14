import unittest

from services.user_service import (
    UserService,
    InvalidUsernameError,
    InvalidPasswordError,
    UsernameExistsError,
    InvalidCredentialsError
)


class FakeUserRepository:
    def __init__(self, users=None):
        self.users = users or []

    def create(self, user):
        user.id = len(self.users) + 1
        self.users.append(user)
        return user

    def find_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService(FakeUserRepository())

    def test_register_with_invalid_username(self):
        with self.assertRaises(InvalidUsernameError):
            self.user_service.register("", "password")

    def test_register_with_valid_username(self):
        user = self.user_service.register("user", "password")
        self.assertEqual(user.username, "user")
        self.assertEqual(user.password, "password")

    def test_register_with_invalid_password(self):
        with self.assertRaises(InvalidPasswordError):
            self.user_service.register("user", "")

    def test_register_with_valid_password(self):
        user = self.user_service.register("user", "password")
        self.assertEqual(user.username, "user")
        self.assertEqual(user.password, "password")

    def test_register_with_existing_username(self):
        self.user_service.register("user", "password")
        with self.assertRaises(UsernameExistsError):
            self.user_service.register("user", "password")

    def test_login_with_invalid_credentials(self):
        with self.assertRaises(InvalidCredentialsError):
            self.user_service.login("invalid", "invalid")

    def test_login_with_valid_credentials(self):
        self.user_service.register("user", "password")
        user = self.user_service.login("user", "password")
        self.assertEqual(user.username, "user")
        self.assertEqual(user.password, "password")
