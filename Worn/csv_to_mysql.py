import pandas as pd
from sqlalchemy import create_engine

# MySQL 접속 정보 입력
user = 'root'          # 사용자명
password = 'skdlem12'   # 비밀번호
host = 'localhost'     # 호스트
port = '3306'          # 포트
database = 'namuwiki'  # 사용할 데이터베이스명

# SQLAlchemy 엔진 생성 (utf8mb4로 명시)
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4",
    connect_args={'charset': 'utf8mb4'}
)

# chunk 단위로 CSV 읽어서 MySQL로 저장
csv_file = "namuwiki_20210301.csv"
chunk_size = 10000  # 한 번에 처리할 행 개수

# 테이블이 이미 있으므로 무조건 append로 저장
for chunk in pd.read_csv(csv_file, chunksize=chunk_size, encoding="utf-8-sig"):
    chunk.to_sql(
        name="namuwiki",
        con=engine,
        if_exists="append",
        index=False
    )
    print(f"{len(chunk)}개 행 업로드 완료")

print("CSV 파일을 MySQL로 모두 업로드했습니다.")