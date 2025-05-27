import sqlite3
import json
import os

def get_clients_info(clients_db_path):
    conn = sqlite3.connect(clients_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT flags, phone FROM clients WHERE flags IS NOT NULL AND phone IS NOT NULL")
    clients = cursor.fetchall()
    conn.close()
    return {str(flags): phone for flags, phone in clients}

# ✅ 연속된 같은 role은 병합하여 1개의 turn으로 처리
def parse_consulting_content(json_path):
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        data = data[0]

    content = data.get("consulting_content", "")
    lines = [line.strip() for line in content.split('\n') if line.strip()]

    merged_turns = []
    current_role = None
    current_texts = []
    turn_no = 0

    for line in lines:
        if line.startswith("상담사:"):
            role = "AGENT"
            text = line.replace("상담사:", "").strip()
        elif line.startswith("손님:"):
            role = "CLIENT"
            text = line.replace("손님:", "").strip()
        else:
            role = "CLIENT"
            text = line.strip()

        if role == current_role:
            current_texts.append(text)
        else:
            if current_role is not None:
                merged_turns.append((turn_no, current_role, '\n'.join(current_texts)))
                turn_no += 1
            current_role = role
            current_texts = [text]

    # 마지막 turn 추가
    if current_texts:
        merged_turns.append((turn_no, current_role, '\n'.join(current_texts)))

    return merged_turns

# ✅ 전체 conversation_log 테이블 비우기
def clear_conversation_log(chats_db_path):
    conn = sqlite3.connect(chats_db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversation_log")
    conn.commit()
    conn.close()
    print("[RESET] conversation_log 테이블 초기화 완료")

# ✅ 대화 로그 삽입
def insert_conversation_log(chats_db_path, source_id, phone, turns):
    conn = sqlite3.connect(chats_db_path)
    cursor = conn.cursor()
    for turn_no, role, text in turns:
        cursor.execute(
            "INSERT INTO conversation_log (source_id, phone, turn_no, role, text) VALUES (?, ?, ?, ?, ?)",
            (source_id, phone, turn_no, role, text)
        )
    conn.commit()
    conn.close()

# ✅ 실행부
if __name__ == "__main__":
    clients_db_path = "./clientsdb/clients.db"
    chats_db_path = "./chatsdb/chats.db"
    origin_dir = "./Data/Origin"

    # 1. 테이블 초기화
    clear_conversation_log(chats_db_path)

    # 2. 클라이언트 목록 조회
    clients_info = get_clients_info(clients_db_path)

    # 3. 각 JSON → DB 삽입
    for source_id, phone in clients_info.items():
        json_path = os.path.join(origin_dir, f"하나카드_{source_id}.json")
        if not os.path.exists(json_path):
            print(f"[SKIP] JSON 파일 없음: {json_path}")
            continue

        try:
            turns = parse_consulting_content(json_path)
            insert_conversation_log(chats_db_path, source_id, phone, turns)
            print(f"[OK] {source_id} 삽입 완료 (총 {len(turns)} turn)")
        except Exception as e:
            print(f"[ERROR] {source_id} 처리 중 오류 발생: {e}")
