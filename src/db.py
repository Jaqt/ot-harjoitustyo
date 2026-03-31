import sqlite3
from config import DATABASE_FILE_PATH


def get_connection():
    con = sqlite3.connect(DATABASE_FILE_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con
