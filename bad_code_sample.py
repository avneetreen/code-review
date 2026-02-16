import os
import sqlite3
from typing import TypedDict

API_KEY = os.environ.get("API_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

def process_user_data(user_id: int, username: str, email: str, phone: str, address: str, country: str, role: str) -> TypedDict:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE id = {user_id} AND name = '{username}'"
    cursor.execute(query)

    try:
        results = cursor.fetchall()
        for row in results:
            print(f"Processing user: {row}")
    except Exception as e:
        print("Something went wrong")

    return results
