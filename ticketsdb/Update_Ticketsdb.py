import os
import json
import sqlite3
import glob
import pprint
import random
from datetime import datetime, timedelta

# # ✅ 0.1. 루트 확인
# import os, json, glob
# source_id = 200001
# classify_dir = "./Data/Classify"

# paths = glob.glob(os.path.join(classify_dir, f"01_분류_{source_id}_*.json"))
# print("찾은 파일:", paths)

# for p in paths:
#     with open(p, encoding='utf-8') as f:
#         data = json.load(f)
#     if isinstance(data, list):
#         data = data[0]
#     print("---", os.path.basename(p))
#     print("task_category -->", data.get("task_category"))
#     print("output        -->", data.get("output"))

# # ✅ 0.15. 루트 고쳤어 다시확인
# src = "./Data/Classify/01_분류_200001_1.json"   # 확인할 파일 경로

# with open(src, encoding="utf-8") as f:
#     data = json.load(f)

# print("👉 최상단 타입:", type(data).__name__)
# if isinstance(data, list):
#     print("👉 리스트 길이 :", len(data))
#     data = data[0]            # 보통 한 덩어리이므로 리스트 첫 요소만 보기
#     print("\n[0] 요소 타입 :", type(data).__name__)

# print("\n👉 최상단 키 목록")
# pprint.pprint(list(data.keys())[:10])          # 많으면 앞 10개만

# # ✅ 0.2. 데이터 출력 확인
# source_id = 200001
# classify_dir = "./Data/Classify"

# # 다섯 개 카테고리 → tickets 칼럼 매핑
# need = {
#     "상담 주제": "category",
#     "상담 요건": "scope",
#     "상담 내용": "type",
#     "상담 사유": "cause",
#     "상담 결과": "result",
# }

# # 결과 저장용 딕셔너리
# result = {v: None for v in need.values()}

# # 해당 source_id에 대한 모든 분류 JSON 순회
# for path in glob.glob(os.path.join(classify_dir, f"01_분류_{source_id}_*.json")):
#     with open(path, encoding="utf-8") as f:
#         data = json.load(f)
#     if isinstance(data, list):
#         data = data[0]

#     task_cat = data.get("task_category")
#     if task_cat in need:
#         result[need[task_cat]] = data.get("output", "").strip()

# # 오류 검증 ─ 하나라도 빠져 있으면 메시지, 아니면 값 출력
# if None in result.values():
#     missing = [k for k, v in result.items() if v is None]
#     print(f"[ERROR] 누락된 항목 → {', '.join(missing)}")
# else:
#     print("=== source_id 200001 티켓 입력 예정 값 ===")
#     for k, v in result.items():
#         print(f"{k:<8} : {v}")


# ✅ 1. 클라이언트 정보 불러오기 (source_id ↔ phone 매핑용)
def load_clients_info(clients_db_path):
    conn = sqlite3.connect(clients_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT source_id, phone FROM clients WHERE source_id IS NOT NULL AND phone IS NOT NULL")
    result = {int(row[0]): row[1] for row in cursor.fetchall()}
    conn.close()
    return result

# ✅ 2. 각 source_id의 최신 상담 시간 가져오기 (conversation_summary에서)
def get_latest_updated_at(chats_db_path):
    conn = sqlite3.connect(chats_db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT source_id, MAX(version), MAX(updated_at) 
        FROM conversation_summary 
        GROUP BY source_id
    """)
    result = {int(row[0]): row[2] for row in cursor.fetchall()}
    conn.close()
    return result

# ✅ 3. 분류 JSON에서 task_category에 맞는 항목 추출
def extract_classification_fields(source_id, classify_dir):
    """source_id 의 모든 01_분류 JSON을 재귀 탐색하여
       5개 칼럼(category·scope·type·cause·result)을 채워서 반환"""
    
    # ① 결과 그릇
    need_map = {
        "상담 주제":  "category",
        "상담 요건":  "scope",
        "상담 내용":  "type",
        "상담 사유":  "cause",
        "상담 결과":  "result",
    }
    result = {v: None for v in need_map.values()}
    
    # ② 재귀 탐색 함수
    def walk(node):
        if isinstance(node, dict):
            if "task_category" in node and "output" in node:
                tc  = node["task_category"]
                out = str(node["output"]).strip()
                if tc in need_map and result[need_map[tc]] is None:
                    result[need_map[tc]] = out
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    
    # ③ 해당 source_id 의 모든 01_분류 파일을 순회·탐색
    pattern = os.path.join(classify_dir, f"01_분류_{source_id}_*.json")
    for path in glob.glob(pattern):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        walk(data)
    
    return result
# 체크
# fields = extract_classification_fields(200001, "./Data/Classify")
# print(fields)

# ✅ 4. 상태(status)를 확률에 따라 생성
def generate_status():
    r = random.random()
    if r < 0.0005:
        return "대기중"
    elif r < 0.001:
        return "처리중"
    return "완료"

# ✅ 5. 생성 시간 및 상태 변경 시간 생성
def generate_timestamps(base_time_str):
    base_time = datetime.strptime(base_time_str, "%Y-%m-%d %H:%M:%S")
    created_at = base_time + timedelta(seconds=random.randint(1, 10))
    updated_at = created_at + timedelta(hours=random.randint(13, 48), minutes=random.randint(0, 59))
    return created_at.strftime("%Y-%m-%d %H:%M:%S"), updated_at.strftime("%Y-%m-%d %H:%M:%S")

# ✅ 6. tickets 테이블 초기화 후 INSERT
def populate_tickets(clients_db, chats_db, tickets_db, classify_dir):
    clients = load_clients_info(clients_db)
    latest_times = get_latest_updated_at(chats_db)

    conn = sqlite3.connect(tickets_db)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tickets")

    ticket_id = 1

    for source_id, phone in clients.items():
        if source_id not in latest_times:
            continue

        classification = extract_classification_fields(source_id, classify_dir)
        if not all(classification.values()):
            print(f"[SKIP] source_id={source_id} → 일부 분류 정보 없음")
            continue

        created_at, updated_at = generate_timestamps(latest_times[source_id])
        status = generate_status()

        cursor.execute("""
            INSERT INTO tickets (
                ticket_id, source_id, phone, category, scope, type, cause, result, 
                status, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            ticket_id, source_id, phone,
            classification["category"], classification["scope"], classification["type"],
            classification["cause"], classification["result"],
            status, created_at, updated_at
        ))

        print(f"[OK] source_id={source_id} → ticket_id={ticket_id}")
        ticket_id += 1

    conn.commit()
    conn.close()

# ✅ 7. 실행 시작점
if __name__ == "__main__":
    # 경로 설정
    clients_db_path = "./clientsdb/clients.db"
    chats_db_path = "./chatsdb/chats.db"
    tickets_db_path = "./ticketsdb/Tickets.db"
    classify_dir = "./Data/Classify"

    # 티켓 생성 실행
    populate_tickets(clients_db_path, chats_db_path, tickets_db_path, classify_dir)
