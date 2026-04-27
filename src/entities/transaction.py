from dataclasses import dataclass


@dataclass
class Transaction:
    """Luokka, joka kuvaa yksittäistä tulo- tai menotapahtumaa

    Attributes:
        user_id: Kokonaisluku, joka kuvaa tapahtuman omistavan käyttäjän tunnistetta
            tietokannassa.
        year: Kokonaisluku, joka kuvaa tapahtuman vuotta.
        month: Kokonaisluku, joka kuvaa tapahtuman kuukautta.
        transaction_type: Merkkijonoarvo, joka kuvaa tapahtuman tyyppiä (tulo tai meno).
        category: Merkkijonoarvo, joka kuvaa tapahtuman kategoriaa.
        amount: Liukuluku, joka kuvaa tapahtuman rahamäärää.
        description:
            Merkkijonoarvo, joka kuvaa tapahtuman kuvausta.
            Oletuksena tyhjä merkkijono.
        id: Kokonaisluku, joka kuvaa tapahtuman yksikäsitteistä tunnistetta
            tietokannassa. Oletuksena None, jolloin tietokantaan tallennettaessa
            luodaan uusi tunniste.
    """

    user_id: int
    year: int
    month: int
    transaction_type: str
    category: str
    amount: float
    description: str = ""
    id: int | None = None
