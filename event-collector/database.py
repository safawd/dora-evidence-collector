import sqlite3
from datetime import datetime

DB_PATH = "dora_events.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            event_type TEXT NOT NULL,
            namespace TEXT,
            resource_name TEXT,
            message TEXT,
            severity TEXT DEFAULT 'INFO',
            raw_data TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée")

def insert_event(source, event_type, namespace, resource_name, message, severity="INFO", raw_data=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO events (timestamp, source, event_type, namespace, resource_name, message, severity, raw_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.utcnow().isoformat(),
        source,
        event_type,
        namespace,
        resource_name,
        message,
        severity,
        raw_data
    ))
    conn.commit()
    conn.close()

def get_all_events():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_events_by_source(source):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM events WHERE source = ? ORDER BY timestamp DESC', (source,))
    rows = cursor.fetchall()
    conn.close()
    return rows
