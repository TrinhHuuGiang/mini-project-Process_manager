'''
Include handler functions for each window:
    + Guide <==
    + CPU/RAM/DISK
    + CPU/RAM/PROC
    + NET/SERVICE
Each function can get return user input into working window.
Then handle and return error code to main.
The 'main' function then decides to process the error code and control the handler functions
'''

'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys
import time
import threading #mutex
import curses

# defined libraries
from _3_display_component.main_window.main_win import Main_win #main class for guide window

# error code
from error_code import *

'''****************************************************************************
* Variable
****************************************************************************'''
# window
w_guide = None

#thread
end_sig = None #default = 1, threadings loop

# keymutex
lock_size = threading.Lock()
    #Synchronize content updates and push content to the screen
    #using mutex 2 threads:
    #- update dynamic window:
    #=> keep safe before push data to buffer screen
    #=> update content with user choice
    #=> sure not print missing content
    #- push content to screen
    #=> keep safe before push data from buffer to screen
    #=> sure push data is not changed

size_not_checked_fisrt_time =None #  default 1 is not check

# dynamic content cycle
cycle_menu_update = 0.2 # 200ms/time update

# push to screen cycle
cycle_screen_refresh = 0.3# 300ms/time for reduce flashing

# main process variable
cycle_user_input = 0.2#200ms

#error code
error_size = None # default = Errorcode.OK , no error size

'''****************************************************************************
* Code
****************************************************************************'''
#renew global variable if recall this window
def renew_global_variable():
    global end_sig
    global size_not_checked_fisrt_time
    global error_size

    end_sig = ErrorCode.NOT_END_SIG
    size_not_checked_fisrt_time = ErrorCode.NOT_CHECKED
    error_size = ErrorCode.OK

# [handler for guide window]
# initialize and check size, set color, set box
# return number order
def init_guide_window():
    global w_guide
    #renew global variables
    renew_global_variable()
    #init guide window object
    w_guide = Main_win()
    #get max number choice
    return w_guide.max_num_choice

# auto handle manu
# -1: quit| 0,1,2,... is order choice
# it can be run as thread but
# i will run it with main process
def update_menu_list_and_get_choice():
    global w_guide
    global end_sig
    # wait user then update or execute or quit 'q'
    temp_input = 'nothing'
    while (temp_input != 'q') and (error_size == ErrorCode.OK):
        # sleep for user react
        time.sleep(cycle_user_input)
        # then check buffer input
        temp_input = w_guide.w_order.getch()
        # if nothing -> compare -1
        if temp_input == -1:
            continue
        # else check what user want
        else: temp_input = chr(temp_input)
        # clean stdin buffer before unlock
        while w_guide.backwin.getch() != -1: continue
        
        if(temp_input == 'w'):
            w_guide.order_top()#user want upper
        elif(temp_input == 's'):
            w_guide.order_down()#user want lower
        elif(temp_input == '\n'):
            #end
            #send end sig
            end_sig = ErrorCode.END_SIG
            #return user chosen
            return w_guide.get_order()#user want order
    
    #end
    end_sig = ErrorCode.END_SIG
    #if input == q
    if temp_input == 'q': return -1 # quit signal
    # error size
    elif error_size == ErrorCode.ERROR_INVALID_MIN_SIZE: return -2 # < size min
    elif error_size == ErrorCode.ERROR_SIZE_CHANGED: return -3 #size changed
    else: return -4

# end
def exit_guide_window():
    global w_guide
    del w_guide #free completely window curses and switch back to the original terminal 
    if debug == ErrorCode.DEBUG:
        print("[OK - {}] closed the guide window".format(exit_guide_window.__name__),
              file=sys.stderr)
    # no return


# ___________[Thread_Function]___________
# Call these support function after init window
# A. Resize window (support)
# check resize or size not invalid
def check_size_valid():
    global w_guide
    global error_size
    global size_not_checked_fisrt_time

    # save old background size
    old_back_col = w_guide.back_win_col
    old_back_row = w_guide.back_win_row

    # [Check size valid]
    # get background size to check change size
    w_guide.get_backwin_size()
    # now check if size invalid
    if((w_guide.back_win_col < w_guide.w_back_mincol) or
    (w_guide.back_win_row < w_guide.w_back_minrow)):
        error_size = ErrorCode.ERROR_INVALID_MIN_SIZE # error size < min

    # [Check if size change]
    if((old_back_col != w_guide.back_win_col) or
    (old_back_row != w_guide.back_win_row)):
        error_size = ErrorCode.ERROR_SIZE_CHANGED # size changed

    # if this is first time checksize, update static content
    if size_not_checked_fisrt_time == ErrorCode.NOT_CHECKED:
        size_not_checked_fisrt_time = ErrorCode.CHECKED#checked

        #and if size ok print static content only one time
        if error_size == ErrorCode.OK :
            #test color
            w_guide.Hello_World()
            #static content
            w_guide.update_guide()
            w_guide.update_background()
    # return error_size code
    return error_size


# B. Update dynamic content
# update menu
def update_menu_list():
    global w_guide
    global end_sig
    global lock_size

    # update menu list
    while(end_sig == ErrorCode.NOT_END_SIG):
        with lock_size:
            #check size screen first before push data to buffer screen
            if check_size_valid() != ErrorCode.OK:
                return #end looping :) end thread
            
            #else update list order
            w_guide.update_order()
        #sleep for other threads and avoid continuous push data to buffer
        time.sleep(cycle_menu_update)

# C. push content to background
def push_to_screen():
    global w_guide
    global end_sig
    global lock_size
    
    #else push content to screen
    while(end_sig == ErrorCode.NOT_END_SIG):
        # push content from buffer to screen
        with lock_size:
            #check size screen first before push data  screen
            if check_size_valid() != ErrorCode.OK:
                return #end looping :) end thread
            #else push to screen
            curses.doupdate()
        #sleep
        time.sleep(cycle_screen_refresh)