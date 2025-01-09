# 구구단 출력 예시 (1단 ~ 9단)
for i in range(1, 10):       # 1부터 9까지
    for j in range(1, 10):   # 1부터 9까지
        print(f"{i} x {j} = {i*j}")
    print()  # 단 사이에 공백 라인 추가