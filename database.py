import sqlite3
from datetime import datetime

DB_PATH = 'vesolje.db'

def init_db():
    """Ustvari tabele če še ne obstajajo (Create tables if not exist)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabela za rezultate (Scores table)
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            points INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    # Tabela za pogovore (Chat history table)
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            reply TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def save_score(name, points):
    """Shrani rezultat v bazo (Save score to database)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO scores (name, points, date) VALUES (?, ?, ?)',
        (name, points, datetime.now().strftime('%d.%m.%Y %H:%M'))
    )
    conn.commit()
    conn.close()

def get_top_scores(limit=10):
    """Pridobi najboljše rezultate (Get top scores)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'SELECT name, points, date FROM scores ORDER BY points DESC LIMIT ?',
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return [{'name': r[0], 'points': r[1], 'date': r[2]} for r in rows]

def save_chat(user, message, reply):
    """Shrani pogovor v bazo (Save chat to database)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        'INSERT INTO chat_history (user, message, reply, date) VALUES (?, ?, ?, ?)',
        (user, message, reply, datetime.now().strftime('%d.%m.%Y %H:%M'))
    )
    conn.commit()
    conn.close()