my_dict = {
    'a': ([1, 2, 3], 10),
    'b': ([4, 5], 15),
    'c': ([6], 8),
    'd': ([7, 8], 20)
}
time_threshold = 16

# 조건에 맞는 항목 필터링 후, 그 중 가장 큰 값 선택
filtered_items = {k: v for k, v in my_dict.items() if v[1] < time_threshold}

if filtered_items:
    last_item = max(filtered_items.items(), key=lambda x: x[1][1])
    print("Last item before time threshold:", last_item)
else:
    print("No item found below the time threshold.")
