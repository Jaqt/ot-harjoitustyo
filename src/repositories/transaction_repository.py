from entities.transaction import Transaction
from db import get_connection


class TransactionRepository:
    """Luokka, joka vastaa tehtäviin liittyvien tietokantaoperaatioiden
        toteuttamisesta.
    """

    def create(self, transaction):
        """Tallentaa uuden tapahtuman tietokantaan.

        Args:
            transaction: Transaction-olio, joka halutaan tallentaa.

        Returns:
            Tallennettu Transaction-olio, joka sisältää tietokannasta
            palautuneet tiedot.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """INSERT INTO transactions (user_id, year, month, transaction_type,
                category, amount, description) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (transaction.user_id, transaction.year, transaction.month,
                 transaction.transaction_type, transaction.category, transaction.amount,
                 transaction.description)
            )
            transaction.id = cursor.lastrowid
            return transaction

    def find_by_user_id(self, user_id):
        """Hakee kaikki tietyn käyttäjän tapahtumat.

            Args:
                user_id: Käyttäjän ID, jonka tapahtumat halutaan hakea.

            Returns:
                Lista Transaction-olioita, jotka kuuluvat kyseiselle käyttäjälle.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT id, user_id, year, month, transaction_type, category,
                amount, description FROM transactions WHERE user_id = ?""",
                (user_id,)
            )
            rows = cursor.fetchall()

            return [
                Transaction(
                    id=row["id"],
                    user_id=row["user_id"],
                    year=row["year"],
                    month=row["month"],
                    transaction_type=row["transaction_type"],
                    category=row["category"],
                    amount=row["amount"],
                    description=row["description"]
                ) for row in rows
            ]

    def find_by_user_and_time(self, user_id, year, month):
        """Hakee tietyn käyttäjän tapahtumat tietyn vuoden ja kuukauden perusteella.

        Args:
            user_id: Käyttäjän ID, jonka tapahtumat halutaan hakea.
            year: Vuosi, jonka tapahtumat halutaan hakea.
            month: Kuukausi, jonka tapahtumat halutaan hakea.

        Returns:
            Lista Transaction-olioita, jotka kuuluvat kyseiselle käyttäjälle
            ja annetulle ajankohdalle.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT id, user_id, year, month, transaction_type, category,
                amount, description FROM transactions WHERE user_id = ? AND 
                year = ? AND month = ?""",
                (user_id, year, month)
            )
            rows = cursor.fetchall()

            return [
                Transaction(
                    id=row["id"],
                    user_id=row["user_id"],
                    year=row["year"],
                    month=row["month"],
                    transaction_type=row["transaction_type"],
                    category=row["category"],
                    amount=row["amount"],
                    description=row["description"]
                ) for row in rows
            ]

    def find_months_by_user_id(self, user_id):
        """Hakee kaikki tietyn käyttäjän tapahtumien vuodet ja kuukaudet.

        Args:
            user_id: Käyttäjän ID, jonka tapahtumien vuodet ja kuukaudet halutaan hakea.

        Returns:
            Lista (vuosi, kuukausi) pareja, joilla käyttäjällä on tapahtumia.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT DISTINCT year, month
                FROM transactions
                WHERE user_id = ?
                ORDER BY year DESC, month DESC
                """,
                (user_id,)
            )
            rows = cursor.fetchall()

            return [(int(row["year"]), int(row["month"])) for row in rows]

    def find_by_transaction_id(self, transaction_id):
        """Hakee tapahtuman sen ID:n perusteella.

        Args:
            transaction_id: Tapahtuman ID, jonka halutaan hakea.

        Returns:
            Transaction-olio, jos löytyy, muuten None.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT id, user_id, year, month, transaction_type, category,
                amount, description FROM transactions WHERE id = ?""",
                (transaction_id,)
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return Transaction(
                id=row["id"],
                user_id=row["user_id"],
                year=row["year"],
                month=row["month"],
                transaction_type=row["transaction_type"],
                category=row["category"],
                amount=row["amount"],
                description=row["description"]
            )

    def delete_all(self):
        """Poistaa kaikki tapahtumat.
        """

        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM transactions")
            connection.commit()
