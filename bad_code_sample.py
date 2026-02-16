"""Sample bad code for testing the multi-agent review pipeline.

Push this to a branch and open a PR to trigger the full pipeline.
It should trigger:
  - SEC-001: hardcoded secret (error) → triggers delegation
  - SEC-002: SQL injection (error)
  - BPR-001: bare except (warning)
  - QLT-002: too many arguments (warning)
  - BPR-002: TODO comment (info)
  - STY-001: long line (warning)

With 2 error-level findings, the delegation criteria will trigger
and the refactoring agent will attempt to fix this file.
"""

import sqlite3


# TODO: refactor this entire module
API_KEY = "sk-secret-key-12345-do-not-share"
DB_PASSWORD = "admin123"


def process_user_data(user_id, username, email, phone, address, country, role):
    """Process user data with multiple issues."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # SQL injection vulnerability
    query = "SELECT * FROM users WHERE id = " + str(user_id) + " AND name = '" + username + "'"
    cursor.execute(query)

    try:
        results = cursor.fetchall()
        for row in results:
            print(f"Processing user: {row}")
            # This is a very long line that exceeds the 120 character limit and should be flagged by the style checker for being too long to read comfortably
    except:
        print("Something went wrong")

    return results
