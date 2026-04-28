from datetime import datetime
from operator import index
from tkinter import ttk, StringVar, constants, messagebox

from constants import MONTHS


class MainView:
    def __init__(self, root, user_service, transaction_service,
                 handle_logout, handle_show_transaction_form):
        self._root = root
        self._user_service = user_service
        self._transaction_service = transaction_service
        self._handle_logout = handle_logout
        self._handle_show_transaction_form = handle_show_transaction_form
        self._frame = None

        self._month_var = StringVar()
        self._month_options = {}
        self._transactions_frame = None

    def _format_month_option(self, year, month):
        year = int(year)
        month = int(month)
        return f"{MONTHS[month - 1]} {year}"

    def _initialize_month_options(self):
        transaction_months = self._transaction_service.get_transaction_months()

        self._month_options = {
            self._format_month_option(year, month): (year, month)
            for year, month in transaction_months
        }

    def _set_default_month(self):
        now = datetime.now()
        current_month_label = self._format_month_option(now.year, now.month)

        if current_month_label in self._month_options:
            self._month_var.set(current_month_label)
        elif self._month_options:
            first_option = list(self._month_options.keys())[0]
            self._month_var.set(first_option)
        else:
            self._month_var.set("")

    def _clear_transactions_frame(self):
        for widget in self._transactions_frame.winfo_children():
            widget.destroy()

    def _show_transactions(self):
        self._clear_transactions_frame()

        selected_label = self._month_var.get()

        if not selected_label:
            no_transactions_label = ttk.Label(
                master=self._transactions_frame,
                text="Ei vielä tapahtumia"
            )
            no_transactions_label.grid(row=0, column=0, sticky=constants.W)
            return

        year, month = self._month_options[selected_label]
        transactions = self._transaction_service.get_transactions_for_month(year, month)

        if not transactions:
            no_transactions_label = ttk.Label(
                master=self._transactions_frame,
                text="Ei vielä tapahtumia"
            )
            no_transactions_label.grid(row=0, column=0, sticky=constants.W)
            return

        for index, transaction in enumerate(transactions):
            text = (
                f"{transaction.month}/{transaction.year} | "
                f"{transaction.transaction_type} | "
                f"{transaction.category} | "
                f"{transaction.amount} € | "
                f"{transaction.description}"
            )

            transaction_label = ttk.Label(
                master=self._transactions_frame,
                text=text
            )
            transaction_label.grid(row=index, column=0, sticky=constants.W, pady=2)

            delete_button = ttk.Button(
                master=self._transactions_frame,
                text="Poista",
                command=lambda transaction_id=transaction.id: self._handle_delete_transaction(transaction_id)
            )
            delete_button.grid(row=index, column=1, sticky=constants.W, padx=10, pady=2)

    def _handle_delete_transaction(self, transaction_id):
        confirm_delete = messagebox.askyesno(
            "Poista tapahtuma",
            "Haluatko varmasti poistaa tapahtuman?"
        )

        if not confirm_delete:
            return

        self._transaction_service.delete_transaction(transaction_id)
        self._show_transactions()

    def _handle_month_change(self, _event):
        self._show_transactions()

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
        content_label.grid(row=1, column=0, pady=20, sticky=constants.W)

        add_transaction_button = ttk.Button(
            master=self._frame,
            text="Lisää uusi tapahtuma",
            command=self._handle_show_transaction_form
        )
        add_transaction_button.grid(row=2, column=0, pady=10, sticky=constants.W)

        self._initialize_month_options()
        self._set_default_month()

        month_combobox = ttk.Combobox(
            master=self._frame,
            textvariable=self._month_var,
            values=list(self._month_options.keys()),
            state="readonly"
        )
        month_combobox.grid(row=3, column=0, pady=10, sticky=constants.W)
        month_combobox.bind("<<ComboboxSelected>>", self._handle_month_change)

        self._transactions_frame = ttk.Frame(master=self._frame)
        self._transactions_frame.grid(row=4, column=0, sticky=(constants.E, constants.W))

        self._show_transactions()

        self._frame.grid(
            column=0,
            row=0,
            sticky=(constants.N, constants.S, constants.E, constants.W)
        )
        top_bar.columnconfigure(0, weight=1)

    def destroy(self):
        self._frame.destroy()
