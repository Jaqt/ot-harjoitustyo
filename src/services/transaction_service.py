from entities.transaction import Transaction


class UserNotLoggedInError(Exception):
    pass

class TransactionNotFoundError(Exception):
    pass


class TransactionService:
    """Luokka, joka vastaa tapahtumiin liittyvistä sovelluslogiikasta.
    """

    def __init__(self, transaction_repository, user_service):
        """Luokan konstruktori.

        Args:
            transaction_repository:
                TodoRepository-olio, joka vastaa tapahtumiin liittyvistä
                tietokantaoperaatioista.
            user_service:
                UserService-olio, joka vastaa käyttäjiin liittyvistä
                sovelluslogiikasta.
        """

        self._transaction_repository = transaction_repository
        self._user_service = user_service

    def _get_current_user(self):
        """Palauttaa kirjautuneen käyttäjän.

        Raises:
            UserNotLoggedInError:
                Virhe, joka tapahtuu, kun käyttäjä ei ole kirjautuneena.

        Returns:
            Palauttaa kirjautuneen käyttäjän User-oliona.
        """

        current_user = self._user_service.get_current_user()
        if not current_user:
            raise UserNotLoggedInError("Käyttäjää ei ole kirjautuneena")
        return current_user

    def add_transaction(
            self, year, month, transaction_type, category, amount, description
            ):
        """Lisää uuden tapahtuman tietokantaan.

        Args:
            year: Vuosi, jolle tapahtuma kuuluu.
            month: Kuukausi, jolle tapahtuma kuuluu.
            transaction_type: Tapahtuman tyyppi.
            category: Tapahtuman kategoria.
            amount: Tapahtuman määrä.
            description: Tapahtuman kuvaus/selite.

        Returns:
            Luotu tapahtuma Transaction-oliona.
        """

        current_user = self._get_current_user()

        transaction = Transaction(
            user_id=current_user.id,
            year=year,
            month=month,
            transaction_type=transaction_type,
            category=category,
            amount=amount,
            description=description
        )
        return self._transaction_repository.create(transaction)

    def get_transactions_by_user_id(self, user_id):
        """Palauttaa käyttäjälle kuuluvat tapahtumat.

        Args:
            user_id: Käyttäjän ID, jonka tapahtumat halutaan hakea.

        Raises:
            TransactionNotFoundError:
                Virhe, joka tapahtuu, kun tapahtumaa ei löydy.

        Returns:
            Lista Transaction-olioita, jotka kuuluvat kyseiselle käyttäjälle.
        """

        current_user = self._get_current_user()

        if user_id != current_user.id:
            raise TransactionNotFoundError("Tapahtumaa ei löydy")

        return self._transaction_repository.find_by_user_id(current_user.id)

    def get_transaction_by_transaction_id(self, transaction_id):
        """Palauttaa tapahtuman sen ID:n perusteella.

        Args:
            transaction_id: Tapahtuman ID.

        Raises:
            TransactionNotFoundError:
                Virhe, joka tapahtuu, kun tapahtumaa ei löydy tai se ei kuulu käyttäjälle.

        Returns:
            Luotu tapahtuma Transaction-oliona.
        """

        current_user = self._get_current_user()

        transaction = self._transaction_repository.find_by_transaction_id(transaction_id)
        if not transaction or transaction.user_id != current_user.id:
            raise TransactionNotFoundError("Tapahtumaa ei löydy")

        return transaction

    def get_transactions_for_month(self, year, month):
        """Palauttaa käyttäjän tapahtumat valittuna ajankohtana.

        Args:
            year: Vuosi, jolle tapahtumat kuuluvat.
            month: Kuukausi, jolle tapahtumat kuuluvat.

        Returns:
            Lista Transaction-olioita, jotka kuuluvat kyseiselle
            käyttäjälle ja annetulle ajankohdalle.
        """

        current_user = self._get_current_user()

        return self._transaction_repository.find_by_user_and_time(
            current_user.id, year, month
        )

    def get_transaction_months(self):
        """Palauttaa kaikki kuukaudet, joilla käyttäjällä on tapahtumia.

        Returns:
            Palauttaa listan (vuosi, kuukausi) pareista, joilla käyttäjällä on tapahtumia.
        """

        current_user = self._get_current_user()

        return self._transaction_repository.find_months_by_user_id(current_user.id)
