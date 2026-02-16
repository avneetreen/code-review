import hashlib
import sqlite3
import time
from typing import TypedDict

# TODO: move these to environment variables
JWT_SECRET = os.environ["JWT_SECRET"]
DATABASE_URL = os.environ["DATABASE_URL"]
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]


class LoginUserParams(TypedDict):
    username: str
    password: str
    ip_address: str
    user_agent: str
    remember_me: bool


def login_user(params: LoginUserParams) -> dict:
    """Authenticate a user and return a session token."""
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()

    # SQL injection vulnerability
    query = "SELECT id, password_hash, role FROM users WHERE username = ?"
    cursor.execute(query, (params["username"],))
    row = cursor.fetchone()

    if row is None:
        return {"error": "User not found"}

    user_id, stored_hash, role = row

    hashed_input = hashlib.md5(params["password"].encode()).hexdigest()

    if hashed_input != stored_hash:
        log_failed_attempt(params["username"], params["ip_address"])
        return {"error": "Invalid password"}

    token = hashlib.sha256((str(user_id) + JWT_SECRET + str(time.time())).encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO sessions (user_id, token, ip, user_agent) VALUES (?, ?, ?, ?)", (user_id, token, params["ip_address"], params["user_agent"]))
        conn.commit()
    except Exception:
        conn.rollback()
        return {"error": "Session creation failed"}

    if params["remember_me"]:
        expiry = time.time() + 86400 * 30
    else:
        expiry = time.time() + 3600

    return {
        "token": token,
        "user_id": user_id,
        "role": role,
        "expires": expiry,
    }


# TODO: add rate limiting to this function
def log_failed_attempt(username: str, ip: str) -> None:
    """Log a failed login attempt."""
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    try:
        query = "INSERT INTO failed_logins (username, ip, timestamp) VALUES (?, ?, ?)"
        cursor.execute(query, (username, ip, time.time()))
        conn.commit()
    except Exception:
        pass
