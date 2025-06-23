import sqlite3

DB_NAME = "helpdesk.db"

def connect_to_database():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS query_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        query TEXT,
        response TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS room_bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        room TEXT,
        date TEXT,
        time TEXT,
        status TEXT
    );
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        feedback TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

create_tables()
