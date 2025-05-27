import sqlite3
import random

DB_PATH = './clientsdb/clients.db'

def add_cardinfo_column():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE clients ADD COLUMN cardinfo TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # 이미 칼럼이 있으면 무시
        pass
    conn.close()

def update_cardinfo():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    card_types = ['A카드', 'B카드', 'C카드', 'D카드']
    cur.execute("SELECT rowid FROM clients")
    rows = cur.fetchall()
    for row in rows:
        cardinfo = random.choice(card_types)
        cur.execute("UPDATE clients SET cardinfo = ? WHERE rowid = ?", (cardinfo, row[0]))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_cardinfo_column()
    update_cardinfo()