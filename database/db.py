import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "spendly.db"


def get_db():
    """Open and return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't already exist."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


def seed_db():
    """Insert demo user and sample expenses — safe to call repeatedly (idempotent)."""
    conn = get_db()
    cur = conn.cursor()

    # Idempotency guard — skip if demo user already exists
    existing = cur.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()
    if existing:
        conn.close()
        return

    # Insert demo user with hashed password
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("password123")),
    )
    user_id = cur.lastrowid

    # 8 sample expenses across all 7 categories
    expenses = [
        (user_id, 12.50,  "Food",          "2025-05-01", "Lunch at cafe"),
        (user_id, 35.00,  "Transport",     "2025-05-03", "Monthly bus pass"),
        (user_id, 120.00, "Bills",         "2025-05-05", "Electricity bill"),
        (user_id, 45.00,  "Health",        "2025-05-08", "Pharmacy"),
        (user_id, 25.00,  "Entertainment", "2025-05-10", "Movie tickets"),
        (user_id, 80.00,  "Shopping",      "2025-05-12", "New shoes"),
        (user_id, 15.00,  "Food",          "2025-05-15", "Groceries"),
        (user_id, 10.00,  "Other",         "2025-05-18", "Miscellaneous"),
    ]
    cur.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )

    conn.commit()
    conn.close()


def create_user(name, email, password):
    """Insert a new user row. Raises sqlite3.IntegrityError on duplicate email."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, generate_password_hash(password)),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id
