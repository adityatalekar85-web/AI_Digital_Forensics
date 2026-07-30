import sqlite3

conn = sqlite3.connect("cyber.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT,

ip TEXT,

country TEXT,

login_status TEXT,

prediction TEXT,

confidence REAL,

date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()


def save_prediction(username, ip, country, login_status, prediction, confidence):

    cursor.execute(
        """
        INSERT INTO predictions
        (username, ip, country, login_status, prediction, confidence)

        VALUES(?,?,?,?,?,?)
        """,
        (
            username,
            ip,
            country,
            login_status,
            prediction,
            confidence
        )
    )

    conn.commit()