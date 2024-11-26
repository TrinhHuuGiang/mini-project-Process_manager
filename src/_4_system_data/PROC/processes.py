'''****************************************************************************
* Definitions
****************************************************************************'''
import psutil
from datetime import datetime

'''****************************************************************************
* Variables, Const
****************************************************************************'''
# Variables for displaying the 'process list'
list_proc = []  # A list of dictionaries containing process information 
                # including "pid", "name", "cpu_percent", "memory_percent", "status", "create_time"
                # Note: "create_time" is converted to the time the process has been running
leng_proc = 0  # Count of processes in the list
sort_order = 0  # Sorting criteria: 0 = pid, 1 = name, 2 = %CPU, 3 = %RAM, 4 = status, 5 = run time

# Variables for 'total system resource' statistics
total_resource_info = None
# {
#     "cpu_percent": 0,  # CPU usage (%)
#     "total_ram": 0,  # Total RAM (MB)
#     "used_ram": 0,  # Used RAM (MB)
#     "current_time": 0,  # Current time
#     "total_pid": 0,  # Total number of processes (PIDs)
#     "running": 0,
#     "sleeping": 0,
#     "stopped": 0,
#     "zombie": 0,
# }

'''****************************************************************************
* CODE
****************************************************************************'''
########## Functions for process list management
def format_elapsed_hhmmss(elapsed_time):
    """Format the elapsed time into hh:mm:ss."""
    seconds = int(elapsed_time.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def sort_by_order():
    '''Sort the process list based on the specified sorting criteria.'''
    global list_proc, sort_order
    if sort_order == 0:  # Sort by PID
        list_proc.sort(key=lambda p: p["pid"])
    elif sort_order == 1:  # Sort by process name
        list_proc.sort(key=lambda p: p["name"].lower())  # Case-insensitive sorting
    elif sort_order == 2:  # Sort by CPU usage (%)
        list_proc.sort(key=lambda p: float(p["cpu_percent"].rstrip('%')), reverse=True)
    elif sort_order == 3:  # Sort by RAM usage (%)
        list_proc.sort(key=lambda p: float(p["memory_percent"].rstrip('%')), reverse=True)
    elif sort_order == 4:  # Sort by process status
        list_proc.sort(key=lambda p: p["status"])
    elif sort_order == 5:  # Sort by runtime
        list_proc.sort(key=lambda p: p["create_time"])
    else:
        return  # No action for invalid sort_order

def get_list_proc():
    '''
    [Retrieve process information]
    Observations indicate that using psutil.process_iter.cache_clear() as suggested at
    https://psutil.readthedocs.io/en/latest/ results in 0% CPU usage being reported.
    This is because CPU usage calculations depend on previously retrieved data.
    '''
    global list_proc
    global leng_proc

    # Reset the process list
    list_proc = []

    # Get the current time
    now = datetime.now()

    # Fetch process data
    for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent", "status", "create_time"]):
        try:
            # Format each process's information
            proc_info = p.info
            proc_info["cpu_percent"] = f"{proc_info['cpu_percent']:.1f}%"  # Format CPU usage
            proc_info["memory_percent"] = f"{proc_info['memory_percent']:.1f}%"  # Format RAM usage

            # Calculate elapsed runtime
            if "create_time" in proc_info and proc_info["create_time"] is not None:
                create_time = datetime.fromtimestamp(proc_info["create_time"])
                elapsed_time = now - create_time
                proc_info["create_time"] = format_elapsed_hhmmss(elapsed_time)

            # Append process information to the list
            list_proc.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Ignore inaccessible processes
            continue

    # Update process count
    leng_proc = len(list_proc)

    # Sort the process list based on the current order
    sort_by_order()

############ Functions for system resource statistics
def get_dict_total_resource():
    '''Collect and organize total system resource statistics.'''
    global total_resource_info

    # Initialize statistics
    total_resource_info = {
        "cpu_percent": 0,  # CPU usage (%)
        "total_ram": 0,  # Total RAM (MB)
        "used_ram": 0,  # Used RAM (MB)
        "current_time": 0,  # Current time
        "total_pid": 0,  # Total number of processes (PIDs)
        "running": 0,
        "sleeping": 0,
        "stopped": 0,
        "zombie": 0,
    }

    # Gather data
    total_resource_info["cpu_percent"] = psutil.cpu_percent(interval=0)
    total_resource_info["total_ram"] = psutil.virtual_memory().total // (1024 ** 2)
    total_resource_info["used_ram"] = psutil.virtual_memory().used // (1024 ** 2)
    total_resource_info["current_time"] = datetime.now().strftime("%H:%M")
    total_resource_info["total_pid"] = len(psutil.pids())

    for proc in psutil.process_iter(['status']):
        try:
            status = proc.info['status']
            if status == psutil.STATUS_RUNNING:
                total_resource_info["running"] += 1
            elif status == psutil.STATUS_SLEEPING:
                total_resource_info["sleeping"] += 1
            elif status == psutil.STATUS_STOPPED:
                total_resource_info["stopped"] += 1
            elif status == psutil.STATUS_ZOMBIE:
                total_resource_info["zombie"] += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
