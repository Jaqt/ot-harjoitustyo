import tkinter as tk

from repositories.user_repository import UserRepository
from services.user_service import UserService
from ui.ui import UI


def main():
    window = tk.Tk()
    window.title("Taloussovellus")
    window.geometry("500x250")

    user_repository = UserRepository()
    user_service = UserService(user_repository)

    ui = UI(window, user_service)
    ui.start()

    window.mainloop()


if __name__ == "__main__":
    main()
