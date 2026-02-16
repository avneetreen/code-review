"""Sample authentication module with multiple code quality issues.

Push this to a branch and open a PR to trigger the multi-agent review pipeline.
Expected findings:
  - SEC-001: hardcoded secrets (error) x2 → triggers delegation
  - SEC-002: SQL injection (error)
  - BPR-001: bare except (warning)
  - QLT-001: function too long (warning) — login_user is >50 lines
  - QLT-002: too many arguments (warning)
  - BPR-002: TODO comments (info) x2
  - STY-001: long lines (warning)
"""

import hashlib
import sqlite3
import time

# TODO: move these to environment variables
JWT_SECRET = "super-secret-jwt-key-2024"
DATABASE_URL = "sqlite:///users.db"
ADMIN_PASSWORD = "P@ssw0rd!admin"


def login_user(username, password, ip_address, user_agent, session_id, remember_me):
    """Authenticate a user and return a session token."""
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()

    # SQL injection vulnerability
    query = "SELECT id, password_hash, role FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    row = cursor.fetchone()

    if row is None:
        return {"error": "User not found"}

    user_id, stored_hash, role = row

    hashed_input = hashlib.md5(password.encode()).hexdigest()

    if hashed_input != stored_hash:
        log_failed_attempt(username, ip_address)
        return {"error": "Invalid password"}

    token = hashlib.md5((str(user_id) + JWT_SECRET + str(time.time())).encode()).hexdigest()

    try:
        cursor.execute("INSERT INTO sessions (user_id, token, ip, user_agent) VALUES ('" + str(user_id) + "', '" + token + "', '" + ip_address + "', '" + user_agent + "')")
        conn.commit()
    except:
        conn.rollback()
        return {"error": "Session creation failed"}

    if remember_me:
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
def log_failed_attempt(username, ip):
    """Log a failed login attempt."""
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    try:
        query = "INSERT INTO failed_logins (username, ip, timestamp) VALUES ('" + username + "', '" + ip + "', '" + str(time.time()) + "')"
        cursor.execute(query)
        conn.commit()
    except:
        pass
