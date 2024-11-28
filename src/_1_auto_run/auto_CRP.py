'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import threading 
import sys

# handler libraries
from _2_display_module.CRP import CRP_window_module, One_proc_window_module

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''
# list module handle of CRP window
CRP_window = [CRP_window_module.init_CRP_window,CRP_window_module.getkey_CRPwindow,
              CRP_window_module.exit_CRP_window]
PID_window = [One_proc_window_module.init_One_proc_window, One_proc_window_module.getkey_One_proc_window,
              One_proc_window_module.exit_One_proc_window]

# list module handle of One process

# threads CRP
CRP_thread1 = None
CRP_thread2 = None
CRP_thread3 = None
CRP_thread4 = None

# threads 1 PID
PID_thread1 = None
PID_thread2 = None
'''****************************************************************************
* Code
****************************************************************************'''
# [Initialize support CRP_threads]
def push_CRP_data_to_screen():
    CRP_window_module.push_to_screen()

def renew_list_precesses_data():
    CRP_window_module.renew_list_precesses_data()

def update_list_proc_display():
    CRP_window_module.update_list_proc_display()

def update_total_resource():
    CRP_window_module.update_total_resource()
    
# start and destroy CRP_threads 
def start_CRP_threads():
    global CRP_thread1
    global CRP_thread2
    global CRP_thread3
    global CRP_thread4

    CRP_thread1 = threading.Thread(target=push_CRP_data_to_screen)
    CRP_thread2 = threading.Thread(target=renew_list_precesses_data)
    CRP_thread3 = threading.Thread(target=update_list_proc_display)
    CRP_thread4 = threading.Thread(target=update_total_resource)

    CRP_thread1.start()
    CRP_thread2.start()
    CRP_thread3.start()
    CRP_thread4.start()

def destroy_CRP_threads():
    global CRP_thread1
    global CRP_thread2
    global CRP_thread3
    global CRP_thread4

    CRP_thread1.join()
    CRP_thread2.join()
    CRP_thread3.join()
    CRP_thread4.join()

# [Initialize support 1_PID_threads]
def push_PID_data_to_screen():
    One_proc_window_module.push_to_screen()
def update_PID_properties():
    One_proc_window_module.update_PID_properties()

# start and destroy 1_PID_threads 
def start_PID_threads():
    global PID_thread1
    global PID_thread2

    PID_thread1 = threading.Thread(target=push_PID_data_to_screen)
    PID_thread2 = threading.Thread(target=update_PID_properties)

    PID_thread1.start()
    PID_thread2.start()

def destroy_PID_threads():
    global PID_thread1
    global PID_thread2

    PID_thread1.join()
    PID_thread2.join()


# [CRP / PID properties auto run]
# It will run processing commands step by step:
# - initialize the CRP screen
# - close the CRP window
# 
# return code:
# (-1) quit
# (< -1) error
# (0) menu
# (1) more PID properties
def CRP_auto_run():
    all_or_one = 0 # 0 is diplay all processes, 1 is display 1 process
    pid_chosen = 0 # default display PID 0 properties
    ret = None # save return error code of function
    while(1):    #loop infinity if no quit or error signal
        # display all by CRP window
        if all_or_one == 0:
            # [CRP handler]
            # initialize display processes window
            CRP_window[0]()
            
            # start create support CRP_threads
            start_CRP_threads()

            # run thread user input
            ret = CRP_window[1]()

            # then end
            # wait all CRP_thread end
            destroy_CRP_threads()

            # close CRP window
            CRP_window[2]()

            # check return
            if(ret >= 0):
                if debug == CommonErrorCode.DEBUG:
                    print("[OK - {}] - Opening PID [{}]".format(CRP_auto_run.__name__,ret), file=sys.stderr)
                # set flag all_or_one
                all_or_one = 1
                pid_chosen = ret

            elif(ret == -1):
                if debug == CommonErrorCode.DEBUG:
                    print("[OK - {}] - Open menu signal".format(CRP_auto_run.__name__), file=sys.stderr)
                return 0
            elif(ret == -2):
                if debug == CommonErrorCode.DEBUG:
                    print("[OK - {}] - Quit signal".format(CRP_auto_run.__name__), file=sys.stderr)
                return -1
            elif (ret < -2):
                if debug == CommonErrorCode.DEBUG:
                    print("[ERR - {}] - Unexpected event (wrong size minimize, size changed,...)".format(CRP_auto_run.__name__), file=sys.stderr)
                return -1
        
        # display 1 process with pid
        elif all_or_one == 1:
            # [1 PID handler]
            # initialize display PID properties window
            # argument 'pid_chosen' for init_One_proc_window(pid)
            PID_window[0](pid_chosen)
            
            # start create support PID_threads
            start_PID_threads()

            # run thread user input
            ret = PID_window[1]()

            # then end
            # wait all CRP_thread end
            destroy_PID_threads()

            # close CRP window
            PID_window[2]()

            # check return
            if(ret == -1):
                if debug == CommonErrorCode.DEBUG:
                    print("[OK - {}] - Opening CRP window [{}]".format(CRP_auto_run.__name__,ret), file=sys.stderr)
                # set flag all_or_one
                all_or_one = 0
                
            elif(ret == -2):
                if debug == CommonErrorCode.DEBUG:
                    print("[OK - {}] - Quit signal".format(CRP_auto_run.__name__), file=sys.stderr)
                return -1
            elif (ret < -2):
                if debug == CommonErrorCode.DEBUG:
                    print("[ERR - {}] - Unexpected event (wrong size minimize, size changed,...)".format(CRP_auto_run.__name__), file=sys.stderr)
                return -1

