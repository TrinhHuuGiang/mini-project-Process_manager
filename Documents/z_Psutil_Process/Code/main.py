import psutil
import os
# def on_terminate(proc):
#     print(f"Process {proc.pid} terminated with exit code {proc.returncode}")
# # Create a list of processes to wait for
# procs = [psutil.Process(pid) for pid in [1,2,3]]
# # Wait for the processes to terminate with a 10-second timeout
# gone, alive = psutil.wait_procs(procs, timeout=10, callback=on_terminate)
# print(f"Terminated processes: {gone}")
# print(f"Still running processes: {alive}")

# try:
#     p = psutil.Process(12345)  # Assuming process with PID 12345 doesn't exist
#     print(p.name())
# except psutil.NoSuchProcess as e:
#     print(f"Process with PID 12345 not found: {e}")
    
# Get the current Python process
p = psutil.Process(psutil.Process().pid)


# Get the user IDs
# uids = p.uids()

# print(f"Real UID: {uids.real}")
# print(f"Effective UID: {uids.effective}")
# print(f"Saved UID: {uids.saved}")

# terminal = p.terminal()

# if terminal:
#     print(f"Process is associated with terminal: {terminal}")
# else:
#     print("Process is not associated with a terminal.")
    

# gids = p.gids()

# print(f"Real GID: {gids.real}")
# print(f"Effective GID: {gids.effective}")
# print(f"Saved GID: {gids.saved}")

# # Get the number of context switches
# ctx_switches = p.num_ctx_switches()

# print(f"Voluntary context switches: {ctx_switches.voluntary}")
# print(f"Involuntary context switches: {ctx_switches.involuntary}")

# num_fds = p.num_fds()

# print(f"Số mô tả tệp của tiến trình: {num_fds}")
# num_threads = p.num_threads()
# print(f"Number of threads : {num_threads}")

# threads = p.threads()

# for thread in threads:
#     print(f"Thread ID: {thread.id}")
#     print(f"User time: {thread.user_time}")
#     print(f"System time: {thread.system_time}")
#     # print(f"Current activity: {thread.current_activity}")
# cpu_times = p.cpu_times()
# print(cpu_times)

# cpu_percent = p.cpu_percent(interval=2)

# print(f"CPU usage: {cpu_percent}%")


print(p.cpu_num())

num_cpus = os.cpu_count()
print("Số lượng CPU:", num_cpus)

# Sử dụng psutil
num_cpus = psutil.cpu_count(logical=True)  # Số lượng CPU logic
print("Số lượng CPU logic:", num_cpus)
num_cpus = psutil.cpu_count(logical=False)  # Số lượng CPU vật lý
print("Số lượng CPU vật lý:", num_cpus)

# memory_maps = p.memory_maps(grouped=True)
# for memory_map in memory_maps:
#     print(f"Path: {memory_map.path}")
#     print(f"RSS: {memory_map.rss / 1024 / 1024:.2f} MB")
#     print(f"Size: {memory_map.size / 1024 / 1024:.2f} MB")
print(p.is_running())