import tkinter as tk

from repositories.user_repository import UserRepository
from repositories.transaction_repository import TransactionRepository
from services.user_service import UserService
from services.transaction_service import TransactionService
from ui.ui import UI


def main():
    """Käynnistää sovelluksen.
    """

    window = tk.Tk()
    window.title("Taloussovellus")
    window.geometry("1024x768")

    user_repository = UserRepository()
    transaction_repository = TransactionRepository()

    user_service = UserService(user_repository)
    transaction_service = TransactionService(transaction_repository, user_service)

    ui = UI(window, user_service, transaction_service)
    ui.start()

    window.mainloop()


if __name__ == "__main__":
    main()
