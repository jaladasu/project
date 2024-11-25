import sqlite3
from encryption import encrypt, decrypt

def init_db():
    connection = sqlite3.connect("aladasu.sqlite")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin1', 'admin123')")
    
    username = "admin2"
    password = "admin123"
    encrypt_pwd = encrypt(password)
    cursor.execute(f"INSERT OR IGNORE INTO users (username, password) VALUES ('{username}', '{encrypt_pwd}')")

    connection.commit()
    connection.close()

def get_db_connection():
    return sqlite3.connect("aladasu.sqlite")
