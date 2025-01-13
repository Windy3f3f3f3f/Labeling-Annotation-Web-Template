# backend/database/db_utils.py
import sqlite3
import os
from config import DATABASE

def get_connection():
    """Get a connection to the database."""
    os.makedirs(os.path.dirname(DATABASE['path']), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE['path'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database."""
    conn = get_connection()
    cur = conn.cursor()

    # Create table: original data table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS annotation_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        textA TEXT NOT NULL,
        textB TEXT NOT NULL,
        is_annotated INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now','localtime'))
    );
    """)

    # Create table: annotation result table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS annotation_result (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_id INTEGER NOT NULL,
        username TEXT NOT NULL,
        score INTEGER NOT NULL,
        timestamp TEXT DEFAULT (datetime('now','localtime')),
        FOREIGN KEY (data_id) REFERENCES annotation_data(id),
        UNIQUE(data_id, username)
    );
    """)

    conn.commit()
    conn.close()
