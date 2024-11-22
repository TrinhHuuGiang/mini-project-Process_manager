import psutil

#duyệt lấy toàn bộ nội dung 5 phần tử
count_p = 200

saved_proc = []

for proc in psutil.process_iter(["pid","name","cpu_percent","memory_percent","status","create_time"]):
    saved_proc.append(proc)
    count_p-=1
    if not count_p:
        break
for proc in saved_proc:
    print(proc)
print(type(saved_proc))



psutil.process_iter.cache_clear() #xoá bộ nhớ đệm nội bộ