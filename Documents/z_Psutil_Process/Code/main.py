import psutil

class ProcessManager:
    def __init__(self):
        self.processes = [] #list process
        self.refresh_processes()
    
    def refresh_processes(self):
        #  refresh processes( update )
        self.processes =  [proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_info', 'status',"username", 'memory_percent', 'cpu_affinity', 'memory_full_info', 'memory_maps', 'num_threads','cwd'])
            for proc in psutil.process_iter()]
                # (['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'username', 'memory_percent'])

    def calculate_total_memory_percent(self):
        # total memory percent (RSS)
        if not self.processes:
            raise ValueError("List process is empty.Call refresh_processes first.")
        return sum(proc['memory_percent'] for proc in self.processes if 'memory_percent' in proc)
    
    def calculage_total_cpu_percent(self):
        if not self.processes:
            raise ValueError("List process is empty.Call refresh_processes first.")
        return sum(proc['cpu_percent'] for proc in self.processes if 'cpu_percent' in proc)
    
    def get_process_by_pid(self, pid): #access process info by pid
        for process in self.processes:
            if process['pid'] == pid:
                return process
        return None
    
    def display_processes(self):
        print(" "*50,f"{self.calculage_total_cpu_percent()}"," "*5,f"{self.calculate_total_memory_percent():.2f} %")
        print(f"{'PID':<10}{'Name':<20}{'Username':<20}{'CPU (%)':<10}{'Memory (RSS)':<15}{'Status':<10} {'CWD'}")
        print("-" * 100)
        for proc in self.processes:
            print(f"{proc['pid']:<10}{proc['name']:<20}{proc['username']:<20}{proc['cpu_percent']:<10.2f}"
                  f"{proc['memory_info'].rss / (1024 * 1024):<15.2f}{proc['status']:<10} {proc['cwd']}")

if __name__ == "__main__":
    pm = ProcessManager()
    pm.display_processes()
    