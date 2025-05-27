import sqlite3
import json

def create_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the tickets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY,
            source_id INTEGER,
            phone TEXT,
            category TEXT,
            scope TEXT,
            type TEXT,
            cause TEXT,
            result TEXT,
            status TEXT,
            created_at DATETIME,
            updated_at DATETIME
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()