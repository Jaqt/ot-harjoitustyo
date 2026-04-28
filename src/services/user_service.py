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
    """Luokka, joka vastaa käyttäjiin liittyvistä sovelluslogiikasta.
    """

    def __init__(self, user_repository):
        """Luokan konstruktori.

        Args:
            user_repository:
                UserRepository-olio, joka vastaa käyttäjiin
                liittyvistä tietokantaoperaatioista.
        """

        self._user_repository = user_repository
        self._user = None

    def get_current_user(self):
        """Palauttaa kirjautuneen käyttäjän.

        Returns:
            Kirjautuneen käyttäjän User-oliona.
        """

        return self._user

    def register(self, username, password):
        """Luo uuden käyttäjän.

        Args:
            username: Käyttäjätunnus, joka halutaan luoda.
            password: Salasana, joka halutaan käyttää.

        Raises:
            InvalidUsernameError:
                Virhe, joka tapahtuu, kun käyttäjätunnus on liian lyhyt.
            InvalidPasswordError:
                Virhe, joka tapahtuu, kun salasana on liian lyhyt.
            UsernameExistsError:
                Virhe, joka tapahtuu, kun käyttäjätunnus on jo olemassa.

        Returns:
            Palauttaa luodun käyttäjän User-oliona.
        """

        username = username.strip()

        if len(username) < 3:
            raise InvalidUsernameError(
                "Käyttäjätunnuksen tulee olla vähintään 3 merkkiä pitkä")

        if len(password) < 3:
            raise InvalidPasswordError(
                "Salasanan tulee olla vähintään 3 merkkiä pitkä")

        existing_user = self._user_repository.find_by_username(username)
        if existing_user:
            raise UsernameExistsError("Käyttäjätunnus on jo olemassa")

        user = User(username, password)
        created_user = self._user_repository.create(user)
        self._user = created_user
        return created_user

    def login(self, username, password):
        """Kirjaa käyttäjän sisään.

        Args:
            username: Käyttäjätunnus, jolla halutaan kirjautua sisään.
            password: Käyttäjän salasana.

        Raises:
            InvalidCredentialsError:
                Virhe, joka tapahtuu, kun käyttäjätunnus tai salasana on väärä.

        Returns:
            Palauttaa kirjautuneen käyttäjän User-oliona.
        """

        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentialsError("Väärä käyttäjätunnus tai salasana")

        self._user = user
        return user

    def logout(self):
        """Kirjaa nykyisen käyttäjän ulos.
        """

        self._user = None
