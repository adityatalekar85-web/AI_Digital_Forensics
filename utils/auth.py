import hashlib
import os
import secrets
import sqlite3
from datetime import datetime

import streamlit as st


DB_PATH = "cyber.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()
    return salt, digest


def ensure_users_table():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'analyst',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

        user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if user_count == 0:
            create_user("admin", "admin123", "Administrator", "admin", conn=conn)


def create_user(username, password, full_name="", role="analyst", conn=None):
    username = username.strip()
    full_name = full_name.strip()

    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    salt, password_digest = hash_password(password)
    owns_connection = conn is None
    conn = conn or get_connection()

    try:
        conn.execute(
            """
            INSERT INTO users(username, password_salt, password_hash, full_name, role, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (username, salt, password_digest, full_name or username, role, datetime.now()),
        )
        conn.commit()
        return True, "Account created successfully. You can login now."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        if owns_connection:
            conn.close()


def authenticate_user(username, password):
    ensure_users_table()
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT username, password_salt, password_hash, full_name, role
            FROM users
            WHERE username = ?
            """,
            (username.strip(),),
        ).fetchone()

    if not row:
        return False, None

    db_username, salt, expected_hash, full_name, role = row
    _, candidate_hash = hash_password(password, salt)

    if not secrets.compare_digest(candidate_hash, expected_hash):
        return False, None

    return True, {
        "username": db_username,
        "full_name": full_name or db_username,
        "role": role or "analyst",
    }


def init_auth_state():
    ensure_users_table()
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None


def require_login():
    init_auth_state()
    if not st.session_state["logged_in"]:
        st.warning("Please login first to access the system.")
        exec(open("pages/login.py", encoding="utf-8").read())
        st.stop()


def current_user():
    init_auth_state()
    return st.session_state.get("user") or {}


def logout_button():
    user = current_user()
    if user:
        st.sidebar.markdown(
            f"""
            <div class="user-chip">
                <span class="user-name">{user.get("full_name", "User")}</span>
                <span class="user-role">{user.get("role", "analyst")}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.sidebar.button("Sign Out", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.rerun()
