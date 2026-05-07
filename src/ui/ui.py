from ui.start_view import StartView
from ui.login_view import LoginView
from ui.register_view import RegisterView
from ui.main_view import MainView
from ui.transaction_form_view import TransactionFormView


class UI:
    def __init__(self, root, user_service, transaction_service):
        self._root = root
        self._user_service = user_service
        self._transaction_service = transaction_service
        self._current_view = None

    def start(self):
        self._show_start_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_start_view(self):
        self._hide_current_view()

        self._current_view = StartView(
            self._root,
            self._show_login_view,
            self._show_register_view
        )

        self._current_view.pack()

    def _show_login_view(self):
        self._hide_current_view()

        self._current_view = LoginView(
            self._root,
            self._user_service,
            self._show_main_view,
            self._show_start_view
        )

        self._current_view.pack()

    def _show_register_view(self):
        self._hide_current_view()

        self._current_view = RegisterView(
            self._root,
            self._user_service,
            self._show_main_view,
            self._show_start_view
        )

        self._current_view.pack()

    def _show_main_view(self):
        self._hide_current_view()

        self._current_view = MainView(
            self._root,
            self._user_service,
            self._transaction_service,
            self._logout,
            self._show_transaction_form_view,
            self._show_edit_transaction_form_view
        )

        self._current_view.pack()

    def _logout(self):
        self._user_service.logout()
        self._show_start_view()

    def _show_transaction_form_view(self):
        self._hide_current_view()

        self._current_view = TransactionFormView(
            self._root,
            self._transaction_service,
            self._user_service,
            self._show_main_view
        )
        self._current_view.pack()

    def _show_edit_transaction_form_view(self, transaction_id):
        self._hide_current_view()

        transaction = self._transaction_service.get_transaction_by_transaction_id(transaction_id)

        self._current_view = TransactionFormView(
            self._root,
            self._transaction_service,
            self._user_service,
            self._show_main_view,
            transaction
        )

        self._current_view.pack()
