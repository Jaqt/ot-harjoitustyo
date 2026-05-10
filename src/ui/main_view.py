import csv
import tkinter as tk
from datetime import datetime
from tkinter import ttk, StringVar, constants, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graphs import create_category_pie_chart
from constants import MONTHS


class MainView:
    """Päänäkymästä vastaava luokka."""

    def __init__(self, root, user_service, transaction_service,
                handle_logout, handle_show_transaction_form,
                handle_show_edit_transaction_form):
        """Luokan konstruktori, joka luo uuden päänäkymän.

        Args:
            root: Tkinterin elementti, johon näkymä asetetaan.
            user_service:
                UserService-olio, joka vastaa käyttäjiin liittyvästä
                sovelluslogiikasta.
            transaction_service:
                TransactionService-olio, joka vastaa tapahtumiin liittyvästä
                sovelluslogiikasta.
            handle_logout: Kutsuttava arvo, joka kirjaa käyttäjän ulos.
            handle_show_transaction_form:
                Kutsuttava arvo, joka näyttää tapahtuman lisäyslomakkeen.
            handle_show_edit_transaction_form:
                Kutsuttava arvo, joka näyttää tapahtuman muokkauslomakkeen.
        """

        self._root = root
        self._user_service = user_service
        self._transaction_service = transaction_service
        self._handle_logout = handle_logout
        self._handle_show_transaction_form = handle_show_transaction_form
        self._handle_show_edit_transaction_form = handle_show_edit_transaction_form
        self._frame = None

        self._month_var = StringVar()
        self._month_options = {}

        self._transactions_container = None
        self._transactions_canvas = None
        self._transactions_canvas_window = None
        self._transactions_scrollbar = None
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

    def _format_description(self, description, max_length=14):
        if not description:
            return ""
        if len(description) <= max_length:
            return description
        return description[:max_length - 3] + "..."

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

        if selected_label not in self._month_options:
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

    def _clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def _show_empty_state(self, year=None, month=None):
        no_transactions_label = ttk.Label(
            master=self._transactions_frame,
            text="Ei vielä tapahtumia."
        )
        no_transactions_label.grid(row=0, column=0, sticky=constants.W)

        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month

        self._show_summary(year, month)
        self._show_category_chart(year, month)

    def _show_transactions(self):
        self._clear_frame(self._transactions_frame)
        self._clear_frame(self._summary_frame)
        self._clear_frame(self._chart_frame)

        selected_label = self._month_var.get()

        if selected_label not in self._month_options:
            self._show_empty_state()
            return

        year, month = self._month_options[selected_label]
        transactions = self._transaction_service.get_transactions_for_month(year, month)

        if not transactions:
            self._show_empty_state(year, month)
            return

        for index, transaction in enumerate(transactions):
            row_frame = ttk.Frame(master=self._transactions_frame)
            row_frame.grid(row=index, column=0, sticky=(constants.W, constants.E), pady=2)

            type_label = ttk.Label(
                master=row_frame,
                text=transaction.transaction_type,
                width=6
            )
            type_label.grid(row=0, column=0, sticky=constants.W, padx=(0, 6))

            category_label = ttk.Label(
                master=row_frame,
                text=transaction.category,
                width=10
            )
            category_label.grid(row=0, column=1, sticky=constants.W, padx=(0, 6))

            amount_label = ttk.Label(
                master=row_frame,
                text=f"{transaction.amount} €",
                width=8
            )
            amount_label.grid(row=0, column=2, sticky=constants.W, padx=(0, 6))

            description_label = ttk.Label(
                master=row_frame,
                text=self._format_description(transaction.description),
                width=14
            )
            description_label.grid(row=0, column=3, sticky=constants.W, padx=(0, 6))

            edit_button = ttk.Button(
                master=row_frame,
                text="Muokkaa",
                command=lambda transaction_id=transaction.id:
                    self._handle_show_edit_transaction_form(transaction_id)
            )
            edit_button.grid(row=0, column=4, sticky=constants.W, padx=(0, 6))

            delete_button = ttk.Button(
                master=row_frame,
                text="Poista",
                command=lambda transaction_id=transaction.id:
                    self._handle_delete_transaction(transaction_id)
            )
            delete_button.grid(row=0, column=5, sticky=constants.W, padx=(0, 6))

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
        self._clear_frame(self._summary_frame)

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
        self._clear_frame(self._chart_frame)

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

        if selected_label not in self._month_options:
            return

        year, month = self._month_options[selected_label]
        self._show_category_chart(year, month)

    def pack(self):
        """Näyttää näkymän."""

        self._frame = ttk.Frame(master=self._root, padding=10)
        self._frame.columnconfigure(0, weight=1)

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

        controls_frame = ttk.Frame(master=self._frame)
        controls_frame.grid(row=3, column=0, pady=10, sticky=constants.W)

        month_combobox = ttk.Combobox(
            master=controls_frame,
            textvariable=self._month_var,
            values=list(self._month_options.keys()),
            state="readonly"
        )
        month_combobox.grid(row=0, column=0, padx=(0, 10), sticky=constants.W)
        month_combobox.bind("<<ComboboxSelected>>", self._handle_month_change)

        export_csv = ttk.Button(
            master=controls_frame,
            text="Vie CSV",
            command=self._handle_export_csv
        )
        export_csv.grid(row=0, column=1, sticky=constants.W)

        content_frame = ttk.Frame(master=self._frame)
        content_frame.grid(row=4, column=0, pady=10, sticky=(constants.W, constants.E))

        content_frame.columnconfigure(0, minsize=520, weight=0)
        content_frame.columnconfigure(1, minsize=320, weight=1)

        self._transactions_container = ttk.LabelFrame(
            master=content_frame,
            text="Tapahtumat",
            padding=10
        )
        self._transactions_container.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky=(constants.N, constants.S, constants.W, constants.E)
        )

        self._transactions_canvas = tk.Canvas(
            master=self._transactions_container,
            height=220
        )

        self._transactions_scrollbar = ttk.Scrollbar(
            master=self._transactions_container,
            orient="vertical",
            command=self._transactions_canvas.yview
        )

        self._transactions_frame = ttk.Frame(master=self._transactions_canvas)
        self._transactions_frame.columnconfigure(0, weight=1)

        self._transactions_frame.bind(
            "<Configure>",
            lambda event: self._transactions_canvas.configure(
                scrollregion=self._transactions_canvas.bbox("all")
            )
        )

        self._transactions_canvas_window = self._transactions_canvas.create_window(
            (0, 0),
            window=self._transactions_frame,
            anchor="nw"
        )

        self._transactions_canvas.configure(
            yscrollcommand=self._transactions_scrollbar.set
        )

        self._transactions_canvas.bind(
            "<Configure>",
            lambda event: self._transactions_canvas.itemconfigure(
                self._transactions_canvas_window,
                width=event.width
            )
        )

        self._transactions_canvas.grid(
            row=0,
            column=0,
            sticky=(constants.N, constants.S, constants.W, constants.E)
        )
        self._transactions_scrollbar.grid(row=0, column=1, sticky=(constants.N, constants.S))

        self._transactions_container.columnconfigure(0, weight=1)
        self._transactions_container.rowconfigure(0, weight=1)

        chart_panel = ttk.LabelFrame(
            master=content_frame,
            text="Kategoriakaavio",
            padding=10
        )
        chart_panel.columnconfigure(0, weight=1)
        chart_panel.grid(
            row=0,
            column=1,
            sticky=constants.N
        )

        chart_type_combobox = ttk.Combobox(
            master=chart_panel,
            textvariable=self._chart_type_var,
            values=["Tulot", "Menot"],
            state="readonly"
        )
        chart_type_combobox.grid(row=0, column=0, pady=(0, 10), sticky=constants.W)
        chart_type_combobox.bind("<<ComboboxSelected>>", self._handle_chart_change)

        self._chart_frame = ttk.Frame(master=chart_panel)
        self._chart_frame.grid(row=1, column=0, sticky=constants.W)

        self._summary_frame = ttk.LabelFrame(
            master=self._frame,
            text="Yhteenveto",
            padding=10
        )
        self._summary_frame.grid(row=5, column=0, pady=10, sticky=(constants.W, constants.E))

        self._show_transactions()

        self._frame.grid(
            column=0,
            row=0,
            sticky=(constants.N, constants.S, constants.E, constants.W)
        )
        top_bar.columnconfigure(0, weight=1)

    def destroy(self):
        """Tuhoaa näkymän."""

        self._frame.destroy()
