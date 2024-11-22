import psutil

#duyệt lấy toàn bộ nội dung 5 phần tử
'''count_p = 10

saved_proc = []

for proc in psutil.process_iter(["pid","name","cpu_percent","memory_percent","status","create_time"]):
    saved_proc.append(proc)
    count_p-=1
    if not count_p:
        break
for proc in saved_proc:
    print(proc.info)
print(type(saved_proc[1]))

psutil.process_iter.cache_clear() #xoá bộ nhớ đệm nội bộ

print("#\n"*5)'''

# truy vấn thông tin 1 đối tượng khi biet pid
'''a_proc = psutil.Process(13)
temp_dict= a_proc.as_dict(attrs=["pid","name","cpu_percent","memory_percent","status","create_time"])
print(temp_dict["pid"]); print(type(temp_dict["pid"]))
'''

# 