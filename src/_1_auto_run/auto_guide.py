'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys
import threading #for

# handler libraries
from _2_display_module import guide_handler

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''
# list function handle of guide window
guide_window = [guide_handler.init_guide_window,guide_handler.update_menu_list_and_get_choice,
guide_handler.exit_guide_window]

# threads
thread1 = None#for loop update list order content
thread2 = None#for loop push content to screen
'''****************************************************************************
* Code
****************************************************************************'''
# [Initialize support threads]
def update_list_order():
    guide_handler.update_menu_list()

def push_content_to_screen():
    guide_handler.push_to_screen()
    
# start and destroy threads 
def start_threads():
    global thread1
    global thread2

    thread1 = threading.Thread(target=update_list_order)
    thread2 = threading.Thread(target=push_content_to_screen)

    thread1.start()
    thread2.start()

def destroy_threads():
    global thread1
    global thread2

    thread1.join()
    thread2.join()

# [guide auto run]
# It will run processing commands step by step:
# - initialize the screen
# - run the menu to take selections from the user
# - close the order window and return the order code.
# return code:
# (-1) user want quit; (<-1) unexpected return ret
# 0,1,2,3... is code of other windows
def guide_auto_run():
    # init variable window
    global guide_window
    ret = 0

    # [guide handler]
    # initialize menu guide window
    max_num_choice = guide_window[0]()
    
    # start create support threads
    start_threads()

    # runs automatically until the user selects a display window
    ret = guide_window[1]()
    if(ret == -1):
        # wait thread end
        destroy_threads()
        # close 'curses' and switch back to the original terminal
        guide_window[2]()
        if debug == ErrorCode.DEBUG:
            print("[OK - {}] - Closed".format(guide_auto_run.__name__), file=sys.stderr)
        return -1 # no error, exit
    elif (ret < 0 ) or (ret >= max_num_choice ):
        # wait thread end
        destroy_threads()
        # close 'curses' and switch back to the original terminal
        guide_window[2]()
        if debug == ErrorCode.DEBUG:
            print("[ERR - {}] - Unexpected event (wrong size minimize, size changed,...)".format(guide_auto_run.__name__), file=sys.stderr)
        return -2 # unexpected ret choice
    
    # else 0<= ret < max_numchoice 
    # wait thread end
    destroy_threads()
    # close the guide window and return the selected event handler
    guide_window[2]()

    # [main will run selected event handler]
    return ret