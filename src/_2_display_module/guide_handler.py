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

'''****************************************************************************
* Variable
****************************************************************************'''
debug = 1# 0 if no debug :)

# window
w_guide = None

# keymutex
lock_size = threading.Lock()
    #Synchronize content updates and push content to the screen
    #using mutex 3 threads:
    #- check size, changed window
    #=> keep safe before print when window invalid size
    #- update dynamic window:
    #=> update content with user choice
    #- push content to screen
    #=> sure not print missing content
end_sig = None #default = 1, threadings loop

#condition variables
condition_wait_checksize = threading.Condition(lock_size)
notify_size_checked = None #default = 1, unchecked
condition_wait_all_wait = threading.Condition(lock_size)
total_waiting = None
max_waiting = 2 # one is dynamic window thread, other is push thread

# check size cycle
cycle_check_resize = 0.01 # 10 ms
# dynamic content cycle
cycle_menu_update = 0.2 # 200ms/time update
# push to screen cycle
cycle_screen_refresh = 0.3# 300ms/time for reduce flashing

# main process variable
cycle_user_input = 0.2#200ms

#error code
error_size = None # default = 0 , no error size

'''****************************************************************************
* Code
****************************************************************************'''
#renew global variable if recall this window
def renew_global_variable():
    global end_sig
    global error_size
    global notify_size_checked
    global total_waiting

    end_sig = 1#end sig = 0 to end thread
    error_size = 0#error_size !=0 if find error
    notify_size_checked = 1#size_checked = 0 is checked
    total_waiting = 0# total will increase after one wait()

# [handler for guide window]
# initialize and check size, set color, set box
# return number order
def init_guide_window():
    global w_guide
    #renew global variables
    renew_global_variable()
    #init guide window object
    w_guide = Main_win()
    #test color
    w_guide.Hello_World()
    #static content
    w_guide.update_guide()
    w_guide.update_background()
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
    while (temp_input != 'q') and (error_size == 0):
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
            end_sig = 0
            return w_guide.get_order()#user want order
    
    #end
    end_sig = 0
    #if input == q
    if temp_input == 'q': return -1 # quit signal
    # error size
    elif error_size == 1: return -2 # < size min
    elif error_size == 2: return -3 #size changed
    else: return -4

# end
def exit_guide_window():
    global w_guide
    del w_guide #free completely window curses and switch back to the original terminal 
    if debug: print("[OK - {}] closed the guide window".format(exit_guide_window.__name__),
                    file=sys.stderr)
    # no return


# ___________[Thread_Function]___________
# Call these support function after init window
# A. Resize window
# check resize or size not invalid
def check_size_valid():
    global w_guide
    global lock_size
    global error_size
    global condition_wait_checksize
    global notify_size_checked
    global condition_wait_all_wait
    global total_waiting

    with lock_size:
        if(max_waiting != total_waiting):
            #wait all thread wait
            condition_wait_all_wait.wait()
    while(end_sig):
        # lock mutex, start check size invalid
        with lock_size:
            # save old background size
            old_back_col = w_guide.back_win_col
            old_back_row = w_guide.back_win_row

            # [Check size valid]
            # get background size to check change size
            w_guide.get_backwin_size()
            # now check if size invalid
            if((w_guide.back_win_col < w_guide.w_back_mincol) or
            (w_guide.back_win_row < w_guide.w_back_minrow)):
                error_size = 1 # error size < min

            # [Check if size change]
            if((old_back_col != w_guide.back_win_col) or
            (old_back_row != w_guide.back_win_row)):
                error_size = 2 # size changed
            
            # else notify other threads (only one time at start)
            if notify_size_checked:
                notify_size_checked = 0
                condition_wait_checksize.notify_all()

        # 10 ms sleep for others thread working
        # then continue check the user suddenly 
        # changes the screen
        time.sleep(cycle_check_resize)

# B. Update dynamic content
# update menu
def update_menu_list():
    global w_guide
    global lock_size
    global error_size
    global condition_wait_checksize
    global total_waiting

    with lock_size:
        #increase total waiting
        total_waiting+=1
        if(total_waiting == max_waiting):
            condition_wait_all_wait.notify()#wake up 'resize check' thread
        #wait check size first time notify all
        condition_wait_checksize.wait()
    #if error size
    if error_size:
        return
    #else update menu list
    while(end_sig):
        with lock_size:
            # update list order
            w_guide.update_order()
        #sleep for other threads and avoid continuous refreshes
        time.sleep(cycle_menu_update)

# C. push content to background
def push_to_screen():
    global w_guide
    global lock_size
    global error_size
    global condition_wait_checksize
    global condition_wait_all_wait
    global total_waiting
    
    with lock_size:
        #increase total waiting
        total_waiting+=1
        if(total_waiting == max_waiting):
            condition_wait_all_wait.notify()#wake up check size first time thread
        #wait check size first time notify all
        condition_wait_checksize.wait()
    #if error size
    if error_size:
        return
    #else push content to screen
    while(end_sig):
        #after time sleep, push content to screen
        with lock_size:
            curses.doupdate()
        #sleep
        time.sleep(cycle_screen_refresh)