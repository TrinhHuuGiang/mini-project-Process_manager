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
# window
w_guide = None

# keymutex
lock_size = threading.Lock()
    #using between
    #- update size window
    #+ keep safe when window invalid size
    #+ re-calculate edge and coordinate
    #+ update static window: guide
    #- update menu:
    #+ update content with user choice
    
# sleep for cpu calculation time
# :) i think this ratio is fine
# sometime get error when we change window size too fast
# resize cycle
sleep_resize_time = 0.01 # 10 ms
# dynamic content cycle
sleep_menu_time = 0.1 # 100ms/time update (~ 10% error when resize)
# static content cycle
sleep_back_time = 0.1 # 100ms/time update (~ 10% error when resize)
# push to screen cycle
screen_refresh_cycle = 0.5# 500ms/time

# main process variable
sleep_get_user_input = 0.4#400ms

'''****************************************************************************
* Code
****************************************************************************'''
# [handler for guide window]
# initialize and check size, set color, set box
# return number order
def init_guide_window():
    global w_guide
    #init guide window object
    w_guide = Main_win()
    #test color
    w_guide.Hello_World()
    #get max number choice
    return w_guide.max_num_choice

# auto handle manu
# -1: quit| 0,1,2,... is order choice
# it can be run as thread but
# i will run it with main process
def update_menu_list_and_get_choice():
    global w_guide
    # wait user then update or execute or quit 'q'
    temp_input = 'nothing'
    while (temp_input != 'q'):
        # sleep for user react
        time.sleep(sleep_get_user_input)
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
            return w_guide.get_order()#user want order
    #if input == q
    return -1 # quit signal

# end
def exit_guide_window():
    global w_guide
    del w_guide #free completely window curses and switch back to the original terminal 
    print("[OK - {}] closed the guide window".format(exit_guide_window.__name__),
    file=sys.stderr)
    # no return


# ___________[Thread_Function]___________
# Call these support function after init window
# A. Resize window
def resize_guide_window():
    global w_guide
    global lock_size
    # 10 ms sleep
    # 10ms is much shorter than 100ms when 'update_order'
    # so it reduces the error rate when the user suddenly 
    # changes the screen size
    time.sleep(sleep_resize_time)
    # save old background size
    old_back_col = w_guide.back_win_col
    old_back_row = w_guide.back_win_row
    # lock mutex, start check and modify size
    with lock_size:
        # [Check size valid]
        # get background size to check change size
        w_guide.get_backwin_size()
        # now check if size invalid
        # loop infinity lock for safe other threads display
        count_before_refresh = 0
        while ((w_guide.back_win_col <= w_guide.w_back_mincol) or
        (w_guide.back_win_row <= w_guide.w_back_minrow)):
            if count_before_refresh == 0:
                count_before_refresh += 1
                # clear then add log error onto menu screen
                w_guide.clear_all_window()
                w_guide.w_order.addstr(0,0,"[Stopped]",w_guide.COS[0])
                w_guide.w_order.addstr(1,0,"80col 24row",w_guide.COS[0])
                w_guide.backwin.noutrefresh()
                # update
                curses.doupdate()#because of 'noutrefresh'
            elif count_before_refresh > 5: count_before_refresh = 0
            else: count_before_refresh +=1
            # combination witch sleep :) for reduce flashing and crash app
            time.sleep(1)#s * count_before_refresh before doupdate
            # now get current size background
            w_guide.get_backwin_size()

        # [Check if size not change]
        if((old_back_col == w_guide.back_win_col) and
        (old_back_row == w_guide.back_win_row)):
            return #size not change/ auto unlock mutex
        
        #[If size valid and changed]
        # mutex before modidy sub window edge
        # calculate, resize all sub window
        w_guide.cal_size_sub_window()
        w_guide.update_size_sub_window()

        #[now renew background after size  changed]
        #clear
        w_guide.backwin.clear()
        #add box
        w_guide.backwin.box('|','-')
        #add name
        w_guide.backwin.addstr(0,1,"[Task Manager]",w_guide.COS[4])
        #noutrefresh to apply new change
        w_guide.backwin.noutrefresh()

        #[update static window]
        #include : guide
        w_guide.update_guide()

# B. Update dynamic content
# update menu
def update_menu_list():
    global w_guide
    global lock_size
    #sleep 100ms for other threads and avoid continuous refreshes
    time.sleep(sleep_menu_time)
    with lock_size:
        # update list order
        w_guide.update_order()

# C. Update static content
    #no sleep, print 1 time after init window
    #so 'no' using 'while loop' when create thread
    #content will update in 'resize_guide_window' when resize
def update_guide_content():
    global w_guide
    global lock_size
    with lock_size:
        w_guide.update_guide()

# update background
def update_background():
    global w_guide
    global lock_size
    time.sleep(sleep_back_time)# wait opening 'Hello'
    with lock_size:
        #add name
        w_guide.backwin.addstr(0,1,"[Task Manager]",w_guide.COS[4])
        #noutrefresh to apply new change
        w_guide.backwin.noutrefresh()

# D. push content to background
def push_to_screen():
    global w_guide
    global lock_size
    time.sleep(screen_refresh_cycle)
    #after time sleep, push content to screen
    with lock_size:
        curses.doupdate()