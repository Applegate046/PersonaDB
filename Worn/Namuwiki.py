from datasets import load_dataset
import pandas as pd

# 나무위키 파켓 파일을 데이터셋으로 불러온다
dataset = load_dataset("parquet", data_files="namuwiki_20210301.parquet")

# train 데이터셋을 판다스 데이터프레임으로 변환
df = pd.DataFrame(dataset["train"])

# 데이터프레임을 CSV 파일로 저장
df.to_csv("namuwiki_20210301.csv", index=False, encoding="utf-8-sig")

# 저장 완료 메시지 출력
print("데이터셋을 namuwiki_20210301.csv 파일로 저장했습니다.")
