import unittest

from services.user_service import UserService, InvalidUsernameError


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
            self.user_service.register("sa", "salasana")
