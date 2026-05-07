from datetime import datetime
from tkinter import ttk, StringVar, constants

from constants import MONTHS, INCOME_CATEGORIES, EXPENSE_CATEGORIES


class TransactionFormView:
    def __init__(
            self, root, transaction_service, user_service,
            handle_back, transaction=None
            ):
        self._root = root
        self._transaction_service = transaction_service
        self._user_service = user_service
        self._handle_back = handle_back
        self._transaction = transaction
        self._frame = None

        if transaction:
            year = transaction.year
            month_name = MONTHS[int(transaction.month) - 1]
            transaction_type = transaction.transaction_type
            category = transaction.category
            amount = str(transaction.amount)
            description = transaction.description or ""
        else:
            now = datetime.now()
            year = now.year
            month_name = MONTHS[now.month - 1]
            transaction_type = "Tulot"
            category = ""
            amount = ""
            description = ""

        self._year_var = StringVar(value=str(year))
        self._month_var = StringVar(value=month_name)
        self._type_var = StringVar(value=transaction_type)
        self._category_var = StringVar(value=category)
        self._amount_var = StringVar(value=amount)
        self._description_var = StringVar(value=description)
        self._message_var = StringVar()

        self._category_combobox = None

    def _get_categories(self):
        if self._type_var.get() == "Tulot":
            return INCOME_CATEGORIES
        return EXPENSE_CATEGORIES

    def _update_categories(self, _event=None):
        categories = self._get_categories()
        self._category_combobox["values"] = categories
        if self._category_var.get() not in categories and categories:
            self._category_var.set(categories[0])

    def _get_month_number(self):
        return MONTHS.index(self._month_var.get()) + 1

    def _handle_save(self):
        try:
            year = int(self._year_var.get())
            month = self._get_month_number()
            transaction_type = self._type_var.get()
            category = self._category_var.get()
            amount = float(self._amount_var.get())
            description = self._description_var.get()

            if self._transaction:
                self._transaction_service.update_transaction(
                    self._transaction.id,
                    year,
                    month,
                    transaction_type,
                    category,
                    amount,
                    description
                )
            else:
                self._transaction_service.add_transaction(
                    year,
                    month,
                    transaction_type,
                    category,
                    amount,
                    description
                )

            self._handle_back()
        except ValueError:
            self._message_var.set("Vuosi ja summa pitää antaa oikeassa muodossa")
        except Exception as error:
            self._message_var.set(str(error))

    def pack(self):
        self._frame = ttk.Frame(master=self._root, padding=10)

        title = "Muokkaa tapahtumaa" if self._transaction else "Lisää tapahtuma"
        title_label = ttk.Label(master=self._frame, text=title)
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        year_label = ttk.Label(master=self._frame, text="Vuosi")
        year_label.grid(row=1, column=0, sticky=constants.W, pady=5)

        year_entry = ttk.Entry(master=self._frame, textvariable=self._year_var)
        year_entry.grid(row=1, column=1, pady=5)

        month_label = ttk.Label(master=self._frame, text="Kuukausi")
        month_label.grid(row=2, column=0, sticky=constants.W, pady=5)

        month_combobox = ttk.Combobox(
            master=self._frame,
            textvariable=self._month_var,
            state="readonly",
            values=MONTHS
        )
        month_combobox.grid(row=2, column=1, pady=5)

        type_label = ttk.Label(master=self._frame, text="Tyyppi")
        type_label.grid(row=3, column=0, sticky=constants.W, pady=5)

        type_combobox = ttk.Combobox(
            master=self._frame,
            textvariable=self._type_var,
            state="readonly",
            values=["Tulot", "Menot"]
        )
        type_combobox.grid(row=3, column=1, pady=5)
        type_combobox.bind("<<ComboboxSelected>>", self._update_categories)

        category_label = ttk.Label(master=self._frame, text="Kategoria")
        category_label.grid(row=4, column=0, sticky=constants.W, pady=5)

        self._category_combobox = ttk.Combobox(
            master=self._frame,
            textvariable=self._category_var,
            state="readonly"
        )
        self._category_combobox.grid(row=4, column=1, pady=5)

        amount_label = ttk.Label(master=self._frame, text="Summa")
        amount_label.grid(row=5, column=0, sticky=constants.W, pady=5)

        amount_entry = ttk.Entry(master=self._frame, textvariable=self._amount_var)
        amount_entry.grid(row=5, column=1, pady=5)

        description_label = ttk.Label(master=self._frame, text="Selite")
        description_label.grid(row=6, column=0, sticky=constants.W, pady=5)

        description_entry = ttk.Entry(master=self._frame, textvariable=self._description_var)
        description_entry.grid(row=6, column=1, pady=5)

        save_button = ttk.Button(master=self._frame, text="Tallenna", command=self._handle_save)
        save_button.grid(row=7, column=0, pady=10)

        back_button = ttk.Button(master=self._frame, text="Takaisin", command=self._handle_back)
        back_button.grid(row=7, column=1, pady=10)

        message_label = ttk.Label(master=self._frame, textvariable=self._message_var)
        message_label.grid(row=8, column=0, columnspan=2, pady=5)

        self._update_categories()

        self._frame.grid(column=0, row=0, sticky=(constants.N, constants.S, constants.E, constants.W))

    def destroy(self):
        self._frame.destroy()
