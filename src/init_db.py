import os

from db import get_connection
from config import DATABASE_FILE_PATH


def delete_database():
    db_path = DATABASE_FILE_PATH

    if os.path.exists(db_path):
        os.remove(db_path)

def create_database(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE users (
            id integer primary key,
            username text,
            password text
        );
    """)

    connection.commit()

def initialize_database():
    delete_database()

    with get_connection() as connection:
        create_database(connection)

if __name__ == "__main__":
    initialize_database()
