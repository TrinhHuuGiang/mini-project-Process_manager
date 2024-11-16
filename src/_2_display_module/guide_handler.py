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
    #- update menu, update guide, update background:
    #+ update content with user choice
    #- update background refresh speed for reduce flashing
    
# sleep for cpu calculation time
# :) i think this ratio is fine
# sometime get error when we change window size too fast
sleep_resize_time = 0.01 # 10 ms
sleep_menu_time = 0.1 # 100ms (~ 10% error)
sleep_guide_time = 0.1 # 100ms (~ 10% error)

# >>>>>>>>>>>>>> [  i think need condition variable here   ] <<<<<<<<<<<<<<<<<<<<<<
# contact background refresh with resize_guide_window()
sleep_back_time = 3 # 3s (no error :) but need modify for reduce flashing)

# main process variable
sleep_get_user_input = 0.1#100ms

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
    # 10 ms sleep
    # 10ms is much shorter than 100ms when 'update_order'
    # so it reduces the error rate when the user suddenly 
    # changes the screen size
    time.sleep(sleep_resize_time)

    global w_guide
    # save old background size
    back_col = w_guide.back_win_col
    back_row = w_guide.back_win_row
    # get background size to check change size
    w_guide.get_backwin_size()
    if((back_col == w_guide.back_win_col) and
       (back_row == w_guide.back_win_row)):
        return #size not change
    
    #[mutex before modidy sub window edge]
    # if size window invalid so lock display any thing
    with lock_size:
        # check min size window
        while((w_guide.back_win_col <=  w_guide.w_back_mincol) or
        (w_guide.back_win_row <= w_guide.w_back_minrow)):
            w_guide.backwin.addstr(0,0,"[Stopped]",w_guide.COS[0])
            # idont know why need refresh before get background size
            # but if don't do it, while will be into infinite loop
            # so great is call refresh before getmaxyx
            # i write an warning the all action will block when size window invalid
            w_guide.backwin.refresh()
            # w_back_minrow may have to be+1 because 
            # sometimes w_guide_begin_col = back_win_col * 10 // 100 may = 1
            w_guide.get_backwin_size()  # dont update size :)
                                        #will error by print addstr out of range
        # when size suitable
        # calculate, resize
        w_guide.cal_size_sub_window()
        w_guide.update_size_sub_window()

        # clean stdin buffer before unlock
        while w_guide.backwin.getch() != -1: continue

# B. Update static content
# update menu
def update_menu_list():
    #sleep 100ms for other threads and avoid continuous refreshes
    time.sleep(sleep_menu_time)
    with lock_size:
        # update list order
        w_guide.update_order()

# update guide
def update_guide_content():
    time.sleep(sleep_guide_time)
    with lock_size:
        w_guide.update_guide()

# update background
def update_background():
    global w_guide
    time.sleep(sleep_back_time)
    with lock_size:
        #clear
        w_guide.backwin.clear()
        #add box
        w_guide.backwin.box('|','-')
        #add name
        w_guide.backwin.addstr(0,1,"[Task Manager]",w_guide.COS[4])
        #refresh to apply new change
        w_guide.backwin.refresh()