from tkinter import ttk, constants


class StartView:
    def __init__(self, root, show_login_view, show_register_view):
        self._root = root
        self._show_login_view = show_login_view
        self._show_register_view = show_register_view
        self._frame = None

    def pack(self):
        self._frame = ttk.Frame(master=self._root, padding=10)

        title_label = ttk.Label(master=self._frame, text="Taloussovellus")
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        login_button = ttk.Button(
            master=self._frame,
            text="Kirjaudu sisään",
            command=self._show_login_view
        )
        login_button.grid(row=1, column=0, padx=5, pady=5)

        register_button = ttk.Button(
            master=self._frame,
            text="Rekisteröidy",
            command=self._show_register_view
        )
        register_button.grid(row=1, column=1, padx=5, pady=5)

        self._frame.grid(column=0, row=0, sticky=(
            constants.N, constants.S, constants.E, constants.W))

    def destroy(self):
        self._frame.destroy()
