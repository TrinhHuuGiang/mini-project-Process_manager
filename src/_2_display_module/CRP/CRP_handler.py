'''
Include handler functions for each window:
    + Guide
    + CPU/RAM/PROC <==
Each function can get return user input into working window.
Then handle and return error code to main.
The 'main' function then decides to process the error code and control the handler functions
'''

'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys
import curses
import time
import threading #mutex

# defined libraries
from _3_display_component.CPU_RAM_PROC.CRP_win import CRPwin #inherit class for CRP window
from _4_system_data.PROC import processes

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''
w_CRP = None

#thread signal
end_sig = None #default = 1, threadings loop

# mutex key
mutex_R1 = threading.Lock()# T1, T2.2, T4.2
mutex_R2 = threading.Lock()# T2.1, T2.2
mutex_R3 = threading.Lock()# T2.1, T2.2, T3.1, T3.2
# thread check user input T3.2 T3.1 (dùng luôn main process)
#mutex_R4  : T4.1 T4.2 bỏ qua

# time cycle
cycle_renew_list_proc = 1 # 1s sleep then renew list processes
cycle_update_list_proc = 0.3 # 300ms sleep then update data list process will display
cycle_renew_and_update_list_total_resource = 1 # 1s sleep then renew and update total resource
cycle_user_input = 0.2 # 200ms sleep then check buffer input
cycle_screen_refresh = 0.3 # 300ms sleep then push data buffer to screen

#check size first time and update static content
size_not_checked_fisrt_time =None #  default CommonErrorCode.NOT_CHECKED

#error code
error_size = None # default = CommonErrorCode.OK , no error size

'''****************************************************************************
* Code
****************************************************************************'''
#renew global variable if recall this window
def renew_global_variable():
    global end_sig
    global size_not_checked_fisrt_time
    global error_size

    end_sig = CommonErrorCode.NOT_END_SIG
    size_not_checked_fisrt_time = CommonErrorCode.NOT_CHECKED
    error_size = CommonErrorCode.OK

# [handler for CPU/RAM/PROC window]
# initialize and check size, set color, set box
def init_CRP_window():
    global w_CRP
    #renew global variables
    renew_global_variable()
    #init guide window object
    w_CRP = CRPwin()

# wait to get key
# main thread combine with T3.1 and T3.2
# resource mutex key R3
def getkey_CRPwindow():
    global w_CRP
    global end_sig
    global mutex_R3
    
    temp_input = "nothing"
    while (temp_input != 'q') and (error_size == CommonErrorCode.OK):
        with mutex_R3:
            # check buffer input
            temp_input = w_CRP.w_proc.getch()
            # if nothing -> compare -1
            if temp_input == -1:
                continue
            # else check what user want
            else: temp_input = chr(temp_input)
            # clean stdin buffer before unlock
            while w_CRP.backwin.getch() != -1: continue
            
            # common signal
            if(temp_input == 'w'):
                w_CRP.move_order_up()#user want upper
            elif(temp_input == 's'):
                w_CRP.move_order_down()#user want lower
            elif(temp_input == '\n'):
                #end
                #send end sig
                end_sig = CommonErrorCode.END_SIG
                #return user chosen(>=0)
                return 0
            
            #sort signal
            elif(temp_input == '0'):
                processes.sort_order = 0
            elif(temp_input == '1'):
                processes.sort_order = 1
            elif(temp_input == '2'):
                processes.sort_order = 2
            elif(temp_input == '3'):
                processes.sort_order = 3
            elif(temp_input == '4'):
                processes.sort_order = 4
            elif(temp_input == '5'):
                processes.sort_order = 5

        # sleep for user react and other thread do
        time.sleep(cycle_user_input)
    #end
    end_sig = CommonErrorCode.END_SIG
    #if input == q
    if temp_input == 'q':
        return -1 # quit signal
    # error size
    elif error_size == CommonErrorCode.ERROR_INVALID_MIN_SIZE:
        return -2 # < size min
    elif error_size == CommonErrorCode.ERROR_SIZE_CHANGED:
        return -3 #size changed
    else:
        return -4

# end
def exit_CRP_window():
    global w_CRP
    del w_CRP #free completely window curses and switch back to the original terminal 
    if debug == CommonErrorCode.DEBUG:
        print("[OK - {}] closed the CRP window".format(exit_CRP_window.__name__),
              file=sys.stderr)
    # no return

# ___________[Thread_Function]___________
# Call these support function after init window
# A. Resize window (support)
# check resize or size not invalid
def check_size_valid():
    global w_CRP
    global error_size
    global size_not_checked_fisrt_time

    # save old background size
    old_back_col = w_CRP.back_win_col
    old_back_row = w_CRP.back_win_row

    # [Check size valid]
    # get background size to check change size
    w_CRP.get_backwin_size()
    # now check if size invalid
    if((w_CRP.back_win_col < w_CRP.w_back_mincol) or
    (w_CRP.back_win_row < w_CRP.w_back_minrow)):
        error_size = CommonErrorCode.ERROR_INVALID_MIN_SIZE # error size < min

    # [Check if size change]
    if((old_back_col != w_CRP.back_win_col) or
    (old_back_row != w_CRP.back_win_row)):
        error_size = CommonErrorCode.ERROR_SIZE_CHANGED # size changed

    # if this is first time checksize, update static content
    if size_not_checked_fisrt_time == CommonErrorCode.NOT_CHECKED:
        size_not_checked_fisrt_time = CommonErrorCode.CHECKED#checked

        #and if size ok print static content only one time
        if error_size == CommonErrorCode.OK :
            #clear all window
            w_CRP.clear_all_window()
            #test color
            w_CRP.Hello_World()
            #static content
            w_CRP.update_background()#do first
            w_CRP.update_guide()

    # return error_size code
    return error_size

# B. push content to background (thread) (T1)
def push_to_screen():
    global w_CRP
    global end_sig
    global mutex_R1
    
    # push content to screen
    while(end_sig == CommonErrorCode.NOT_END_SIG):
        # push content from buffer to screen
        with mutex_R1:
            #check size screen first before push data  screen
            if check_size_valid() != CommonErrorCode.OK:
                return #end looping :) end thread
            #else push to screen
            curses.doupdate()
        #sleep
        time.sleep(cycle_screen_refresh)

# C. Renew processes list data (thread) (T2.1) 
def renew_list_precesses_data():
    global w_CRP
    global end_sig
    global mutex_R2
    global mutex_R3

    while(end_sig == CommonErrorCode.NOT_END_SIG):
        with mutex_R2:
            with mutex_R3:
                #check size screen first before push data  screen
                if check_size_valid() != CommonErrorCode.OK:
                    return #end looping :) end thread
                #else renew list proc
                w_CRP.renew_list_processes()
        #then unlock R2 + R3
        #sleep
        time.sleep(cycle_renew_list_proc)

# D. Release data processes will display to buffer (thread) (T2.2)
def update_list_proc_display():
    global w_CRP
    global end_sig
    global mutex_R1
    global mutex_R2
    global mutex_R3

    while(end_sig == CommonErrorCode.NOT_END_SIG):
        with mutex_R1:
            with mutex_R2:
                with mutex_R3:
                    #check size screen first before push data  screen
                    if check_size_valid() != CommonErrorCode.OK:
                        return #end looping :) end thread
                    #else renew list proc
                    w_CRP.update_proc_content()
        #then unlock R1 + R2 + R3
        #sleep
        time.sleep(cycle_update_list_proc)

# E. Release data total resource will display to buffer (thread) (T4.1+T4.2)
def update_total_resource():
    global w_CRP
    global end_sig
    global mutex_R1

    while(end_sig == CommonErrorCode.NOT_END_SIG):
        with mutex_R1:
            #check size screen first before push data  screen
            if check_size_valid() != CommonErrorCode.OK:
                return #end looping :) end thread
            #else renew list proc
            w_CRP.update_total_content()
        #then unlock R1
        #sleep
        time.sleep(cycle_renew_and_update_list_total_resource)