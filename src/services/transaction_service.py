from entities.transaction import Transaction


class UserNotLoggedInError(Exception):
    pass

class TransactionNotFoundError(Exception):
    pass


class TransactionService:
    def __init__(self, transaction_repository, user_service):
        self._transaction_repository = transaction_repository
        self._user_service = user_service

    def add_transaction(self, year, month, transaction_type, category, amount,
                        description):
        current_user = self._user_service.get_current_user()
        if not current_user:
            raise UserNotLoggedInError("Käyttäjää ei ole kirjautuneena")

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
        current_user = self._user_service.get_current_user()
        if not current_user:
            raise UserNotLoggedInError("Käyttäjää ei ole kirjautuneena")

        if user_id != current_user.id:
            raise TransactionNotFoundError("Tapahtumaa ei löydy")

        transactions = self._transaction_repository.find_by_user_id(user_id)
        return transactions

    def get_transaction_by_transaction_id(self, transaction_id):
        current_user = self._user_service.get_current_user()
        if not current_user:
            raise UserNotLoggedInError("Käyttäjää ei ole kirjautuneena")

        transaction = self._transaction_repository.find_by_transaction_id(transaction_id)
        if not transaction or transaction.user_id != current_user.id:
            raise TransactionNotFoundError("Tapahtumaa ei löydy")

        return transaction

    def get_transactions_for_month(self, year, month):
        current_user = self._user_service.get_current_user()
        if not current_user:
            raise UserNotLoggedInError("Käyttäjää ei ole kirjautuneena")

        return self._transaction_repository.find_by_user_and_time(
            current_user.id, year, month
        )

    def get_transaction_months(self):
        current_user = self._user_service.get_current_user()
        if not current_user:
            raise UserNotLoggedInError("Käyttäjää ei ole kirjautuneena")

        return self._transaction_repository.find_months_by_user_id(current_user.id)
