# database.py
import sqlite3
from config import DATABASE_FILE

def init_db():
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic_id INTEGER NOT NULL,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )''')
        conn.commit()

def add_topic(topic_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO topics (topic_id) VALUES (?)', (topic_id,))
        conn.commit()

def get_topics():
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute('SELECT topic_id FROM topics ORDER BY last_activity DESC')
        topics = c.fetchall()
        return [topic[0] for topic in topics]

def update_topic_activity(topic_id):
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute('UPDATE topics SET last_activity=CURRENT_TIMESTAMP WHERE topic_id=?', (topic_id,))
        conn.commit()

def get_least_active_topic():
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute('SELECT topic_id FROM topics ORDER BY last_activity ASC LIMIT 1')
        topic = c.fetchone()
        return topic[0] if topic else None

def get_topic_count():
    with sqlite3.connect(DATABASE_FILE) as conn:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM topics')
        count = c.fetchone()[0]
        return count