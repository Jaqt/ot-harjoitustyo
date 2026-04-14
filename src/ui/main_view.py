from tkinter import ttk, constants


class MainView:
    def __init__(self, root, user_service, transaction_service,
                 handle_logout, handle_show_transaction_form):
        self._root = root
        self._user_service = user_service
        self._transaction_service = transaction_service
        self._handle_logout = handle_logout
        self._handle_show_transaction_form = handle_show_transaction_form
        self._frame = None

    def pack(self):
        self._frame = ttk.Frame(master=self._root, padding=10)

        current_user = self._user_service.get_current_user()

        top_bar = ttk.Frame(master=self._frame)
        top_bar.grid(row=0, column=0, sticky=(constants.E, constants.W))

        welcome_label = ttk.Label(
            master=top_bar,
            text=f"Tervetuloa, {current_user.username}!"
        )
        welcome_label.grid(row=0, column=0, sticky=constants.W)

        logout_button = ttk.Button(
            master=top_bar,
            text="Kirjaudu ulos",
            command=self._handle_logout
        )
        logout_button.grid(row=0, column=1, sticky=constants.E, padx=10)

        content_label = ttk.Label(
            master=self._frame,
            text="Yhteenveto"
        )
        content_label.grid(row=1, column=0, pady=30)

        add_transaction_button = ttk.Button(
            master=self._frame,
            text="Lisää kuukausitapahtuma",
            command=self._handle_show_transaction_form
        )
        add_transaction_button.grid(row=2, column=0, pady=10)

        transactions_frame = ttk.Frame(master=self._frame)
        transactions_frame.grid(row=3, column=0, sticky=(constants.E, constants.W))

        transactions = self._transaction_service.get_transactions_by_user_id(current_user.id)

        if not transactions:
            no_transactions_label = ttk.Label(
                master=transactions_frame,
                text="Ei vielä tapahtumia"
            )
            no_transactions_label.grid(row=0, column=0, sticky=constants.W)
        else:
            for index, transaction in enumerate(transactions):
                text = (
                    f"{transaction.month}/{transaction.year} | "
                    f"{transaction.transaction_type} | "
                    f"{transaction.category} | "
                    f"{transaction.amount} € | "
                    f"{transaction.description}"
                )

                transaction_label = ttk.Label(
                    master=transactions_frame,
                    text=text
                )
                transaction_label.grid(row=index, column=0, sticky=constants.W, pady=2)

        self._frame.grid(column=0, row=0, sticky=(
            constants.N, constants.S, constants.E, constants.W))
        top_bar.columnconfigure(0, weight=1)

    def destroy(self):
        self._frame.destroy()
