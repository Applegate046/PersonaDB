# 하나카드 AI 상담 데이터베이스 프로젝트

## 프로젝트 개요
이 프로젝트는 하나카드 상담 데이터를 체계적으로 관리하고, AI/데이터 분석에 활용할 수 있도록 다양한 데이터베이스(DB)와 자동화 스크립트를 제공합니다.  
상담 원본, 분류 결과, 클라이언트 정보 등 여러 데이터를 SQLite DB로 정리하며, 각 단계별로 Python 스크립트가 준비되어 있습니다.

---

## 전체 폴더 및 파일 구조

```
Team_Project/
└── Dev/
    ├── chatsdb/
    │   ├── Create_Chatsdb.py         # 상담 로그 DB 생성 및 데이터 입력
    │   └── chats.db                  # 상담 로그 DB 파일 (자동 생성)
    │
    ├── clientsdb/
    │   ├── Update_clients.py         # 클라이언트 정보 DB 갱신 및 source_id 추가
    │   ├── Update_cardinfo.py        # cardinfo 칼럼 추가 및 임의 카드 정보 입력
    │   └── clients.db                # 클라이언트 DB 파일 (자동 생성)
    │
    ├── ticketsdb/
    │   ├── Create_Ticketsdb.py       # 티켓 DB 생성
    │   ├── Update_Ticketsdb.py       # 티켓 DB에 데이터 입력 및 갱신
    │   └── tickets.db                # 티켓 DB 파일 (자동 생성)
    │
    ├── Data/
    │   ├── Origin/                   # 상담 원본 JSON 파일 저장 폴더
    │   │   └── 하나카드_*.json       # 각 상담별 원본 파일 (예: 하나카드_1.json)
    │   ├── Classify/                 # 분류 결과 JSON 파일 저장 폴더
    │   │   └── 01_분류_*.json        # 분류 결과 파일 (예: 01_분류_200001_1.json)
    │   ├── Summary/                  # 상담 요약 JSON 파일 저장 폴더
    │   │   └── summary_*.json        # 상담 요약 파일 (예: summary_200001.json)
    │   └── (기타 데이터 파일)
    │
    ├── requirements.txt              # 프로젝트 의존성 명시 파일
    └── Readme.md                     # 프로젝트 설명서 (본 파일)
```

---

## 각 폴더 및 파일 설명

### 1. chatsdb/
- **Create_Chatsdb.py**  
  `clients.db`에서 클라이언트 정보를 읽고, `Data/Origin/`의 상담 JSON 파일을 파싱하여  
  `chats.db`의 `conversation_log` 테이블에 상담 대화 내용을 저장합니다.
- **chats.db**  
  상담 대화 로그가 저장되는 SQLite DB 파일입니다. 스크립트 실행 시 자동 생성됩니다.

### 2. clientsdb/
- **Update_clients.py**  
  `clients.db`에 `source_id` 칼럼을 추가하고, 각 JSON 파일에서 `source_id`를 읽어와  
  `flags` 값과 매칭하여 DB에 업데이트합니다. 또한, 성별/나이 등 클라이언트 정보를 자동으로 채웁니다.
- **Update_cardinfo.py**  
  `clients.db`에 `cardinfo`라는 새로운 칼럼을 추가하고,  
  기존 모든 클라이언트 데이터에 대해 'A카드', 'B카드', 'C카드', 'D카드' 중 하나의 카드명을 임의로 입력합니다.
- **clients.db**  
  클라이언트 정보가 저장되는 SQLite DB 파일입니다. 스크립트 실행 시 자동 생성됩니다.

### 3. ticketsdb/
- **Create_Ticketsdb.py**  
  `tickets` 테이블을 생성하는 스크립트입니다.
- **Update_Ticketsdb.py**  
  `Data/Classify/`의 분류 JSON 파일을 재귀적으로 탐색하여  
  각 상담별로 5개 항목(category, scope, type, cause, result)을 추출,  
  `tickets.db`의 `tickets` 테이블에 티켓 정보를 생성 및 갱신합니다.
- **tickets.db**  
  티켓 정보가 저장되는 SQLite DB 파일입니다. 스크립트 실행 시 자동 생성됩니다.

### 4. Data/
- **Origin/**  
  상담 원본 JSON 파일(`하나카드_*.json`)을 저장하는 폴더입니다.  
  각 파일에는 상담의 전체 내용, 클라이언트 정보 등이 포함되어 있습니다.
- **Classify/**  
  분류 결과 JSON 파일(`01_분류_*.json`)을 저장하는 폴더입니다.  
  각 파일에는 상담의 분류 결과(주제, 요건, 내용, 사유, 결과 등)가 포함되어 있습니다.
- **Summary/**  
  상담 요약 JSON 파일(`summary_*.json`)을 저장하는 폴더입니다.  
  각 파일에는 상담의 요약 정보가 포함되어 있습니다. 예시:  
  - 상담 전체 내용 요약  
  - 주요 이슈 및 해결 방안  
  - 상담의 핵심 키워드 등  
  파일명 예시: `summary_200001.json` (source_id 기준)

### 5. requirements.txt
- 프로젝트 실행에 필요한 Python 버전 및 패키지(외부 패키지는 없고, 표준 라이브러리만 사용)를 명시합니다.

### 6. Readme.md
- 프로젝트 전체 설명, 폴더 구조, 실행 방법, 문의처 등을 안내합니다.

---

## 데이터 준비 방법

1. **상담 원본 데이터**  
   `./Data/Origin/` 폴더에 `하나카드_1.json`, `하나카드_2.json` 등 상담별 JSON 파일을 넣으세요.

2. **분류 결과 데이터**  
   `./Data/Classify/` 폴더에 `01_분류_200001_1.json` 등 분류 결과 JSON 파일을 넣으세요.

3. **상담 요약 데이터**  
   `./Data/Summary/` 폴더에 `summary_200001.json` 등 상담 요약 JSON 파일을 넣으세요.

---

## 실행 순서 및 방법

1. **클라이언트 DB 준비 및 업데이트**
    ```bash
    python ./clientsdb/Update_clients.py
    ```
    - `clients.db` 파일이 생성되고, 각 클라이언트의 성별/나이/source_id 정보가 자동으로 채워집니다.

2. **카드 정보 칼럼 추가 및 임의 데이터 입력**
    ```bash
    python ./clientsdb/Update_cardinfo.py
    ```
    - `clients.db`에 `cardinfo` 칼럼이 추가되고, 모든 클라이언트에 대해 임의의 카드명이 입력됩니다.

3. **상담 로그 DB 생성**
    ```bash
    python ./chatsdb/Create_Chatsdb.py
    ```
    - `chats.db` 파일이 생성되고, 상담 대화 로그가 저장됩니다.

4. **티켓 DB 생성**
    ```bash
    python ./ticketsdb/Create_Ticketsdb.py
    ```
    - `tickets.db` 파일이 생성되고, 티켓 테이블이 준비됩니다.

5. **티켓 정보 입력 및 갱신**
    ```bash
    python ./ticketsdb/Update_Ticketsdb.py
    ```
    - 분류 결과를 바탕으로 티켓 정보가 DB에 입력됩니다.

---

## requirements.txt 예시

```
python>=3.8
# 외부 패키지 필요 없음 (모두 표준 라이브러리 사용)
```

---

## 참고 및 주의사항

- 각 스크립트 실행 전, 데이터 파일 경로와 DB 파일 위치를 반드시 확인하세요.
- DB 파일이 이미 존재하면 일부 스크립트는 기존 데이터를 덮어쓸 수 있습니다.
- Python 3.8 이상, SQLite3, 표준 라이브러리만 사용합니다.
- 데이터 파일명 규칙(`하나카드_*.json`, `01_분류_*.json`, `summary_*.json`)을 반드시 지켜주세요.
- `Data/Summary/` 폴더의 요약 데이터는 향후 분석, 검색, 리포트 등에 활용할 수 있습니다.

---

## 문의

- 담당자: 김현우
- 문의: applegate046@gmail.com