import os
import pandas as pd

# file_path=os.path.join(os.getcwd(),"data","CollegeMsg.txt")
file_path=os.path.join(os.getcwd(),"data","bitcoin.txt")
df=pd.read_csv(file_path,sep=" ",header=None,names=["source","target","time"])

# source와 target 컬럼의 고유값 합치기
unique_nodes = pd.unique(df[["source", "target"]].values.ravel())

# 오름차순 정렬
sorted_nodes = sorted(unique_nodes)

# 차이 계산 (연속된 1인지 확인)
diffs = [b - a for a, b in zip(sorted_nodes[:-1], sorted_nodes[1:])]

# 모두 1인지 확인
is_sequential = all(d == 1 for d in diffs)

print("정확히 1씩 증가:", is_sequential)