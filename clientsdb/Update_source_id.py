import os
import json
import sqlite3
import re

DATA_DIR = './Data/Origin/'
DB_PATH = './clientsdb/clients.db'

def ensure_column_exists(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(clients)")
    columns = [col[1] for col in cursor.fetchall()]
    if "source_id" not in columns:
        cursor.execute("ALTER TABLE clients ADD COLUMN source_id TEXT")
        conn.commit()

def update_source_id():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    ensure_column_exists(conn)

    files = [f for f in os.listdir(DATA_DIR) if f.startswith('하나카드_') and f.endswith('.json')]
    for fname in files:
        match = re.search(r'하나카드_(\d+)\.json', fname)
        if not match:
            continue
        flags = int(match.group(1))
        path = os.path.join(DATA_DIR, fname)
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
            item = data[0] if isinstance(data, list) else data
            source_id = item.get('source_id')
            if source_id:
                cur.execute(
                    "UPDATE clients SET source_id = ? WHERE flags = ?",
                    (str(source_id), flags)
                )
                print(f"[OK] flags={flags} → source_id={source_id}")
            else:
                print(f"[SKIP] {fname}: 'source_id' not found in JSON")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_source_id()
