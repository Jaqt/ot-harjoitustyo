class User:
    """Luokka, joka kuvaa yksittäistä käyttäjää.

    Attributes:
        id: Kokonaisluku, joka kuvaa käyttäjän yksikäsitteistä tunnistetta tietokannassa.
        username: Merkkijonoarvo, joka kuvaa käyttäjän käyttäjätunnusta.
        password: Merkkijonoarvo, joka kuvaa käyttäjän salasanaa.
    """

    def __init__(self, username, password, user_id=None):
        """Luokan konstruktori, joka luo uuden käyttäjäolion.

        Args:
            username: Merkkijonoarvo, joka kuvaa käyttäjän käyttäjätunnusta.
            password: Merkkijonoarvo, joka kuvaa käyttäjän salasanaa.
            user_id:
                Kokonaisluku, joka kuvaa käyttäjän yksikäsitteistä tunnistetta
                tietokannassa. Oletuksena None, jolloin tietokantaan tallennettaessa
                luodaan uusi tunniste.
        """

        self.id = user_id
        self.username = username
        self.password = password
