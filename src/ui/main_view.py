import csv
from datetime import datetime
from tkinter import ttk, StringVar, constants, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graphs import create_category_pie_chart
from constants import MONTHS


class MainView:
    def __init__(self, root, user_service, transaction_service,
                handle_logout, handle_show_transaction_form,
                handle_show_edit_transaction_form):
        self._root = root
        self._user_service = user_service
        self._transaction_service = transaction_service
        self._handle_logout = handle_logout
        self._handle_show_transaction_form = handle_show_transaction_form
        self._handle_show_edit_transaction_form = handle_show_edit_transaction_form
        self._frame = None

        self._month_var = StringVar()
        self._month_options = {}
        self._transactions_frame = None
        self._summary_frame = None

        self._chart_type_var = StringVar(value="Tulot")
        self._chart_frame = None

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

    def _handle_export_csv(self):
        selected_label = self._month_var.get()

        if not selected_label:
            messagebox.showinfo("Vie CSV", "Ei vietävää kuukautta valittuna.")
            return

        year, month = self._month_options[selected_label]
        header, rows = self._transaction_service.get_csv_export_data_for_month(year, month)

        if not rows:
            messagebox.showinfo("Vie CSV", "Valitulla kuukaudella ei ole tapahtumia.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV-tiedostot", "*.csv")],
            initialfile=f"tapahtumat_{year}_{month}.csv"
        )

        if not filepath:
            return

        with open(filepath, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

        messagebox.showinfo("Vie CSV", "Kuukausijakson tapahtumat tallennettu tiedostoon.")

    def _clear_transactions_frame(self):
        for widget in self._transactions_frame.winfo_children():
            widget.destroy()

    def _clear_summary_frame(self):
        for widget in self._summary_frame.winfo_children():
            widget.destroy()

    def _clear_chart_frame(self):
        for widget in self._chart_frame.winfo_children():
            widget.destroy()

    def _show_transactions(self):
        self._clear_transactions_frame()
        self._clear_summary_frame()
        self._clear_chart_frame()

        selected_label = self._month_var.get()

        if not selected_label:
            no_transactions_label = ttk.Label(
                master=self._transactions_frame,
                text="Ei vielä tapahtumia"
            )
            no_transactions_label.grid(row=0, column=0, sticky=constants.W)

            now = datetime.now()
            self._show_summary(now.year, now.month)
            self._show_category_chart(now.year, now.month)
            return

        year, month = self._month_options[selected_label]
        transactions = self._transaction_service.get_transactions_for_month(year, month)

        if not transactions:
            no_transactions_label = ttk.Label(
                master=self._transactions_frame,
                text="Ei vielä tapahtumia"
            )
            no_transactions_label.grid(row=0, column=0, sticky=constants.W)

            self._show_summary(year, month)
            self._show_category_chart(year, month)
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

            edit_button = ttk.Button(
                master=self._transactions_frame,
                text="Muokkaa",
                command=lambda transaction_id=transaction.id:
                    self._handle_show_edit_transaction_form(transaction_id)
            )
            edit_button.grid(row=index, column=1, sticky=constants.W, padx=10, pady=2)

            delete_button = ttk.Button(
                master=self._transactions_frame,
                text="Poista",
                command=lambda transaction_id=transaction.id:
                    self._handle_delete_transaction(transaction_id)
            )
            delete_button.grid(row=index, column=2, sticky=constants.W, padx=10, pady=2)

        self._show_summary(year, month)
        self._show_category_chart(year, month)

    def _handle_month_change(self, _event):
        self._show_transactions()

    def _handle_delete_transaction(self, transaction_id):
        confirm_delete = messagebox.askyesno(
            "Poista tapahtuma",
            "Haluatko varmasti poistaa tapahtuman?"
        )

        if not confirm_delete:
            return

        self._transaction_service.delete_transaction(transaction_id)
        self._show_transactions()

    def _show_summary(self, year, month):
        self._clear_summary_frame()

        income_total, expense_total = self._transaction_service.get_summary_for_month(year, month)

        summary_title = ttk.Label(
            master=self._summary_frame,
            text="Kuukausijakson yhteenveto",
            font=("Arial", 12, "bold")
        )
        summary_title.grid(row=0, column=0, sticky=constants.W, pady=(10, 5))

        income_label = ttk.Label(
            master=self._summary_frame,
            text=f"Tulot yhteensä: {income_total} €"
        )
        income_label.grid(row=1, column=0, sticky=constants.W)

        expense_label = ttk.Label(
            master=self._summary_frame,
            text=f"Menot yhteensä: {expense_total} €"
        )
        expense_label.grid(row=1, column=1, sticky=constants.W)

    def _show_category_chart(self, year, month):
        self._clear_chart_frame()

        transaction_type = self._chart_type_var.get()
        labels, values = self._transaction_service.get_category_distribution_for_month(
            year, month, transaction_type
        )

        if not values:
            if transaction_type == "Tulot":
                message = "Ei tuloja valitulla kuukaudella."
            else:
                message = "Ei menoja valitulla kuukaudella."
            no_chart_label = ttk.Label(
                master=self._chart_frame,
                text=message
            )
            no_chart_label.grid(row=0, column=0, sticky=constants.W)
            return

        figure = create_category_pie_chart(labels, values, transaction_type)

        canvas = FigureCanvasTkAgg(figure, master=self._chart_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(constants.W, constants.E))

    def _handle_chart_change(self, _event):
        selected_label = self._month_var.get()

        if not selected_label:
            return

        year, month = self._month_options[selected_label]
        self._show_category_chart(year, month)

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
            text="Tilanne",
            font=("Arial", 14, "bold")
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

        export_csv = ttk.Button(
            master=self._frame,
            text="Vie CSV",
            command=self._handle_export_csv
        )
        export_csv.grid(row=3, column=1, pady=10, sticky=constants.W)

        self._transactions_frame = ttk.Frame(master=self._frame)
        self._transactions_frame.grid(row=4, column=0, sticky=(constants.E, constants.W))

        self._summary_frame = ttk.Frame(master=self._frame)
        self._summary_frame.grid(row=5, column=0, pady=10, sticky=(constants.E, constants.W))

        chart_type_combobox = ttk.Combobox(
            master=self._frame,
            textvariable=self._chart_type_var,
            values=["Tulot", "Menot"],
            state="readonly"
        )
        chart_type_combobox.grid(row=6, column=0, pady=10, sticky=constants.W)
        chart_type_combobox.bind("<<ComboboxSelected>>", self._handle_chart_change)

        self._chart_frame = ttk.Frame(master=self._frame)
        self._chart_frame.grid(
            row=7, column=0, columnspan=2, pady=10, sticky=(constants.W, constants.E)
        )

        self._show_transactions()

        self._frame.grid(
            column=0,
            row=0,
            sticky=(constants.N, constants.S, constants.E, constants.W)
        )
        top_bar.columnconfigure(0, weight=1)

    def destroy(self):
        self._frame.destroy()
