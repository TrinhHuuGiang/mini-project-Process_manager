'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys
import threading #for

# handler libraries
from _2_display_module.menu import menu_window_module

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''
# list function handle of menu window
menu_window = [menu_window_module.init_menu_window,menu_window_module.get_choice_and_return,
menu_window_module.exit_menu_window]

# threads
thread1 = None#for loop update list order content
thread2 = None#for loop push content to screen
'''****************************************************************************
* Code
****************************************************************************'''
# [Initialize support threads]
def update_menu_list():
    menu_window_module.update_menu_list()

def push_to_screen():
    menu_window_module.push_to_screen()
    
# start and destroy threads 
def start_threads():
    global thread1
    global thread2

    thread1 = threading.Thread(target=update_menu_list)
    thread2 = threading.Thread(target=push_to_screen)

    thread1.start()
    thread2.start()

def destroy_threads():
    global thread1
    global thread2

    thread1.join()
    thread2.join()

# [menu auto run]
# It will run processing commands step by step:
# - initialize the screen
# - run the menu to take selections from the user
# - close the order window and return the order code.
# return code:
# (-1) user want quit; (<-1) unexpected return ret
# 0,1,2,3... is code of other windows
def menu_auto_run():
    # init variable window
    global menu_window
    ret = None

    # [menu handler]
    # initialize menu menu window
    max_num_choice = menu_window[0]()
    
    # start create support threads
    start_threads()

    # runs automatically until the user selects a display window
    ret = menu_window[1]()

    # then end
    # wait thread end
    destroy_threads()

    # close the menu window and check the selected event handler
    menu_window[2]()

    if(ret == -1):
        if debug == CommonErrorCode.DEBUG:
            print("[OK - {}] - Quit signal".format(menu_auto_run.__name__), file=sys.stderr)
    elif (ret < -1 ) or (ret >= max_num_choice ):
        if debug == CommonErrorCode.DEBUG:
            print("[ERR - {}] - Unexpected event (wrong size minimize, size changed,...)".format(menu_auto_run.__name__), file=sys.stderr)
    
    # else 0<= ret < max_numchoice
    
    # [main will run selected event handler]
    return ret