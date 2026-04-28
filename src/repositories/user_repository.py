from entities.user import User
from db import get_connection


class UserRepository:
    """Luokka, joka vastaa käyttäjiin liittyvien tietokantaoperaatioiden
        toteuttamisesta.
    """

    def create(self, user):
        """Tallentaa uuden käyttäjän tietokantaan.

        Args:
            user: User-olio, joka halutaan tallentaa.

        Returns:
            Tallennettu käyttäjä User-oliona.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (user.username, user.password)
            )
            user.id = cursor.lastrowid
            return user

    def find_by_username(self, username):
        """Hakee käyttäjän sen käyttäjätunnuksen perusteella.

        Args:
            username: Käyttäjätunnus, jonka halutaan hakea.

        Returns:
            Käyttäjä User-oliona, jos löytyy, muuten None.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return User(
                username=row["username"],
                password=row["password"],
                user_id=row["id"]
            )

    def delete_all(self):
        """Poistaa kaikki käyttäjät.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users")
            connection.commit()
