'''****************************************************************************
* Definitions
****************************************************************************'''
import psutil
from datetime import datetime, timedelta

'''****************************************************************************
* Variables, Const
****************************************************************************'''
list_proc = []  # list dictionary is limited by offset and number ordered 
                # include "pid", "name", "cpu_percent", "memory_percent", "status", "create_time"
                # but "create_time" was changed mean is time process has been run
leng_proc = 0 # c, số phần tử trong list process
sort_order = 0 # 0: pid, 1: name, 2:%cpu, 3: %RAM, 4: status, 5: create time
'''****************************************************************************
* CODE
****************************************************************************'''
def format_elapsed_hhmmss(elapsed_time):
    """Định dạng thời gian chạy thành chuỗi hh:mm:ss."""
    seconds = int(elapsed_time.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def sort_by_order():
    '''dựa theo order ta có thể xắp xếp thứ tự danh sách theo tiêu chí'''
    global list_proc, sort_order
    if sort_order == 0:  # Sắp xếp theo PID
        list_proc.sort(key=lambda p: p["pid"])
    elif sort_order == 1:  # Sắp xếp theo tên tiến trình (name)
        list_proc.sort(key=lambda p: p["name"].lower())  # Sử dụng .lower() để không phân biệt hoa/thường
    elif sort_order == 2:  # Sắp xếp theo CPU %
        list_proc.sort(key=lambda p: float(p["cpu_percent"].rstrip('%')), reverse=True)  # Sắp xếp giảm dần
    elif sort_order == 3:  # Sắp xếp theo RAM %
        list_proc.sort(key=lambda p: float(p["memory_percent"].rstrip('%')), reverse=True)  # Sắp xếp giảm dần
    elif sort_order == 4:  # Sắp xếp theo trạng thái tiến trình (status)
        list_proc.sort(key=lambda p: p["status"])
    elif sort_order == 5:  # Sắp xếp theo thời gian chạy (create_time)
        list_proc.sort(key=lambda p: p["create_time"])  # Thời gian dạng chuỗi hh:mm:ss
    else:
        return  # Nếu không hợp lệ, không làm gì

def get_list_proc():
    '''
    [lấy thông tin tiến trình]
    khi thực nghiệm thấy rằng nếu dùng psutil.process_iter.cache_clear() theo đề xuất
    từ https://psutil.readthedocs.io/en/latest/
    thì cpu in ra luôn là 0 %
    lý do là vì khi tính cpu cần dựa vào dữ liệu trước đó lấy được
    '''
    global list_proc
    global leng_proc

    # Reset
    list_proc = []

    # Thời gian hiện tại
    now = datetime.now()

    # Get data
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status", "create_time"]):
        try:
            # Định dạng thông tin của mỗi tiến trình
            proc_info = p.info
            proc_info["cpu_percent"] = f"{proc_info['cpu_percent']:.2f}%"  # Định dạng CPU %
            proc_info["memory_percent"] = f"{proc_info['memory_percent']:.2f}%"  # Định dạng Memory %

            # Tính thời gian đã chạy
            if "create_time" in proc_info and proc_info["create_time"] is not None:
                create_time = datetime.fromtimestamp(proc_info["create_time"])
                elapsed_time = now - create_time
                proc_info["create_time"] = format_elapsed_hhmmss(elapsed_time)  # Định dạng thời gian đã chạy

            # Thêm thông tin vào danh sách
            list_proc.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Bỏ qua các tiến trình không thể truy cập
            continue
    
    # Clear psutil internal cache
    # psutil.process_iter.cache_clear()

    # Get length
    leng_proc = len(list_proc)

    #sort by order
    sort_by_order()