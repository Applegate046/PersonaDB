import sqlite3

conn = sqlite3.connect('./clients.db')
cur = conn.cursor()

# phone이 NULL이고, id가 6533 초과인 데이터 삭제
cur.execute("DELETE FROM clients WHERE phone IS NULL")

conn.commit()
cur.close()
conn.close()