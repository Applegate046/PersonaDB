import os
import json
import sqlite3
import random
import re

DATA_DIR = './Data/'
DB_PATH = './clients.db'

def parse_age(age_str):
    if age_str == "30대":
        return random.randint(30, 39)
    elif age_str == "20대":
        return random.randint(20, 29)
    elif age_str == "40대":
        return random.randint(40, 49)
    elif age_str == "60대":
        return random.randint(60, 69)
    elif age_str == "10대":
        return random.randint(10, 19)
    elif age_str == "50대":
        return random.randint(50, 59)
    elif age_str == "70대":
        return random.randint(70, 79)
    else:
        return None

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 비어있는 gender, age, flags를 가진 행을 모두 가져옴
    cur.execute("SELECT rowid FROM clients WHERE gender IS NULL OR age IS NULL OR flags IS NULL")
    rows = cur.fetchall()

    files = [f for f in os.listdir(DATA_DIR) if f.startswith('하나카드_') and f.endswith('.json')]
    files = sorted(files)

    for idx, fname in enumerate(files):
        if idx >= len(rows):
            break
        rowid = rows[idx][0]
        match = re.search(r'하나카드_(\d+)\.json', fname)
        flag_value = int(match.group(1)) if match else None

        with open(os.path.join(DATA_DIR, fname), encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                item = data[0]
            else:
                item = data
            gender = item.get('client_gender')
            age_str = item.get('client_age')
            age = parse_age(age_str)
            if gender and age and flag_value is not None:
                cur.execute(
                    "UPDATE clients SET gender = ?, age = ?, flags = ? WHERE rowid = ?",
                    (gender, age, flag_value, rowid)
                )
    conn.commit()
    conn.close()

def add_source_id_column():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # 이미 칼럼이 있으면 에러가 나므로 try-except 사용
    try:
        cur.execute("ALTER TABLE clients ADD COLUMN source_id TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # 이미 칼럼이 있으면 무시
    conn.close()

if __name__ == '__main__':
    add_source_id_column()
    main()
