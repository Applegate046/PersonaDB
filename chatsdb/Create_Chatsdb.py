import sqlite3
import json
import os

def get_clients_info(clients_db_path):
    conn = sqlite3.connect(clients_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT flags, phone FROM clients")
    clients = cursor.fetchall()
    conn.close()
    return {str(flags): phone for flags, phone in clients}

def parse_consulting_content(json_path):
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    result = []
    if isinstance(data, list):
        # 리스트의 각 항목에 대해 처리
        for item in data:
            content = item.get("consulting_content", "")
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            for idx, line in enumerate(lines):
                if line.startswith("상담사:"):
                    role = "AGENT"
                    text = line.replace("상담사:", "").strip()
                elif line.startswith("손님:"):
                    role = "CLIENT"
                    text = line.replace("손님:", "").strip()
                else:
                    role = "CLIENT"
                    text = line.strip()
                result.append((idx, role, text))
    else:
        # 기존 dict 처리
        content = data.get("consulting_content", "")
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        for idx, line in enumerate(lines):
            if line.startswith("상담사:"):
                role = "AGENT"
                text = line.replace("상담사:", "").strip()
            elif line.startswith("손님:"):
                role = "CLIENT"
                text = line.replace("손님:", "").strip()
            else:
                role = "CLIENT"
                text = line.strip()
            result.append((idx, role, text))
    return result

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

if __name__ == "__main__":
    clients_db_path = "./clientsdb/clients.db"
    chats_db_path = "./chatsdb/chats.db"
    origin_dir = "./Data/Origin"

    clients_info = get_clients_info(clients_db_path)
    for source_id, phone in clients_info.items():
        json_path = os.path.join(origin_dir, f"하나카드_{source_id}.json")
        if not os.path.exists(json_path):
            continue
        turns = parse_consulting_content(json_path)
        insert_conversation_log(chats_db_path, source_id, phone, turns)
