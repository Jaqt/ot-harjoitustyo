from tkinter import ttk, StringVar, constants
from services.user_service import InvalidCredentialsError


class LoginView:
    def __init__(self, root, user_service, show_main_view, show_start_view):
        self._root = root
        self._user_service = user_service
        self._show_main_view = show_main_view
        self._show_start_view = show_start_view

        self._frame = None
        self._username_var = StringVar()
        self._password_var = StringVar()
        self._message_var = StringVar()

    def _handle_login(self):
        username = self._username_var.get()
        password = self._password_var.get()

        try:
            self._user_service.login(username, password)
            self._show_main_view()
        except InvalidCredentialsError as error:
            self._message_var.set(str(error))

    def pack(self):
        self._frame = ttk.Frame(master=self._root, padding=10)

        title_label = ttk.Label(master=self._frame, text="Kirjaudu sisään")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        username_label = ttk.Label(master=self._frame, text="Käyttäjätunnus")
        username_label.grid(row=1, column=0, sticky=constants.W, pady=5)

        username_entry = ttk.Entry(master=self._frame, textvariable=self._username_var)
        username_entry.grid(row=1, column=1, pady=5)

        password_label = ttk.Label(master=self._frame, text="Salasana")
        password_label.grid(row=2, column=0, sticky=constants.W, pady=5)

        password_entry = ttk.Entry(master=self._frame, textvariable=self._password_var, show="*")
        password_entry.grid(row=2, column=1, pady=5)

        login_button = ttk.Button(master=self._frame, text="Kirjaudu", command=self._handle_login)
        login_button.grid(row=3, column=0, pady=10)

        back_button = ttk.Button(master=self._frame, text="Takaisin", command=self._show_start_view)
        back_button.grid(row=3, column=1, pady=10)

        message_label = ttk.Label(master=self._frame, textvariable=self._message_var)
        message_label.grid(row=4, column=0, columnspan=2, pady=5)

        self._frame.grid(column=0, row=0, sticky=(constants.N, constants.S, constants.E, constants.W))

    def destroy(self):
        self._frame.destroy()