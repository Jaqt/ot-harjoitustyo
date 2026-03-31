from entities.user import User


class UsernameExistsError(Exception):
    pass

class InvalidCredentialsError(Exception):
    pass

class InvalidUsernameError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

class UserService:
    def __init__(self, user_repository):
        self._user_repository = user_repository
        self._user = None

    def get_current_user(self):
        return self._user

    def register(self, username, password):
        username = username.strip()

        if len(username) < 3:
            raise InvalidUsernameError("Käyttäjätunnuksen tulee olla vähintään 3 merkkiä pitkä")

        if len(password) < 3:
            raise InvalidPasswordError("Salasanan tulee olla vähintään 3 merkkiä pitkä")

        existing_user = self._user_repository.find_by_username(username)
        if existing_user:
            raise UsernameExistsError("Käyttäjätunnus on jo olemassa")

        user = User(username, password)
        created_user = self._user_repository.create(user)
        self._user = created_user
        return created_user

    def login(self, username, password):
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentialsError("Väärä käyttäjätunnus tai salasana")

        self._user = user
        return user

    def logout(self):
        self._user = None