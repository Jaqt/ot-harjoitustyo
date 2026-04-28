import os

from db import get_connection
from config import DATABASE_FILE_PATH


def delete_database():
    """Poistaa vanhan tietokantatiedoston, jos se on olemassa.
    """

    db_path = DATABASE_FILE_PATH

    if os.path.exists(db_path):
        os.remove(db_path)


def create_tables(connection):
    """Luo tietokantataulut.
    """

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    connection.commit()


def initialize_database():
    """Alustaa tietokannan.
    """

    delete_database()

    with get_connection() as connection:
        create_tables(connection)


if __name__ == "__main__":
    initialize_database()
