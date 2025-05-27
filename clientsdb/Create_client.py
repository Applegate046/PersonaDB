from faker import Faker
import random
import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('./clientdb/clients.db')
cur = conn.cursor()

# 중복 방지를 위한 집합
names = set()
phones = set()
target_count = 6533  # 원하는 데이터 개수
inserted = 5896

for i in range(4154):
    fake = Faker("ko_KR")
    # 랜덤 번호 생성
    phone = f'010{random.randint(0, 9999):04d}{random.randint(0, 9999):04d}'
    name = fake.name()
    # 중복 체크
    if name in names or phone in phones:
        continue
    names.add(name)
    phones.add(phone)
    # DB에 삽입
    try:
        cur.execute("INSERT INTO clients (name, phone) VALUES (?, ?)", (name, phone))
        inserted += 1
    except sqlite3.IntegrityError:
        continue

conn.commit()
cur.close()
conn.close()