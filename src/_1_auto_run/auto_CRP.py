'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import threading 

# handler libraries
from _2_display_module.CRP import CRP_window_module

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''
# list function handle of CRP window
CRP_window = [CRP_window_module.init_CRP_window,CRP_window_module.getkey_CRPwindow,
              CRP_window_module.exit_CRP_window]

# threads
thread1 = None
thread2 = None
thread3 = None
thread4 = None
'''****************************************************************************
* Code
****************************************************************************'''
# [Initialize support threads]
def push_to_screen():
    CRP_window_module.push_to_screen()

def renew_list_precesses_data():
    CRP_window_module.renew_list_precesses_data()

def update_list_proc_display():
    CRP_window_module.update_list_proc_display()

def update_total_resource():
    CRP_window_module.update_total_resource()
    
# start and destroy threads 
def start_threads():
    global thread1
    global thread2
    global thread3
    global thread4

    thread1 = threading.Thread(target=push_to_screen)
    thread2 = threading.Thread(target=renew_list_precesses_data)
    thread3 = threading.Thread(target=update_list_proc_display)
    thread4 = threading.Thread(target=update_total_resource)

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

def destroy_threads():
    global thread1
    global thread2
    global thread3
    global thread4

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()


# [CRP auto run]
# It will run processing commands step by step:
# - initialize the CRP screen
# - close the CRP window
# return code:
# (-1) window too small
def CRP_auto_run():
    ret = None
    # [guide handler]
    # initialize display process window
    CRP_window[0]()
    
    # start create support threads
    start_threads()

    #else wait use type some thing
    ret = CRP_window[1]()

    # then end
    # wait thread end
    destroy_threads()


    #return terminal to re open menu
    CRP_window[2]()
    
    #exit ok
    return ret
