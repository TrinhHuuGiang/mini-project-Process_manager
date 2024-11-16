'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys
import threading #for

# handler libraries
from _2_display_module import guide_handler

'''****************************************************************************
* Variable
****************************************************************************'''
# list function handle of guide window
guide_window = [guide_handler.init_guide_window,guide_handler.update_menu_list_and_get_choice,
guide_handler.exit_guide_window]

# global signal for thread
end_sig = 1

# threads
thread1 = None
thread2 = None
thread3 = None
thread4 = None
'''****************************************************************************
* Code
****************************************************************************'''
# [Initialize support threads]
def resize_win():
    global end_sig
    while end_sig:
        guide_handler.resize_guide_window()

def update_list_order():
    global end_sig
    while end_sig:
        guide_handler.update_menu_list()

def update_guide():
    global end_sig
    while end_sig:
        guide_handler.update_guide_content()

def update_background():
    global end_sig
    while end_sig:
        guide_handler.update_background()
    
# start and destroy threads 
def start_threads():
    global thread1,thread2, thread3, thread4
    thread1 = threading.Thread(target=resize_win)
    thread2 = threading.Thread(target=update_list_order)
    thread3 = threading.Thread(target=update_guide)
    thread4 = threading.Thread(target=update_background)

    thread1.start() # resize always start first
    thread2.start()
    thread3.start()
    thread4.start()

def destroy_threads():
    global thread1,thread2, thread3, thread4
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

# [guide auto run]
# It will run processing commands step by step:
# - initialize the screen
# - run the menu to take selections from the user
# - close the order window and return the order code.
# return code:
# (-1) user want quit; (-2) unexpected return ret
# 0,1,2,3... is code of other windows
def guide_auto_run():
    # init variable window
    global guide_window
    ret = 0
    # init variable threads
    global end_sig

    # [guide handler]
    # initialize menu guide window
    max_num_choice = guide_window[0]()
    
    # start create support threads
    start_threads()

    # runs automatically until the user selects a display window
    ret = guide_window[1]()
    if(ret == -1):
        # wait thread end
        end_sig = 0
        destroy_threads()
        # close 'curses' and switch back to the original terminal
        guide_window[2]()
        print("[OK - {}] - Closed".format(guide_auto_run.__name__), file=sys.stderr)
        return -1 # no error, exit
    elif((ret < 0 ) and (ret >= max_num_choice )):
        # wait thread end
        end_sig = 0
        destroy_threads()
        # close 'curses' and switch back to the original terminal
        guide_window[2]()
        print("[ERR - {}] - Unexpected event".format(guide_auto_run.__name__), file=sys.stderr)
        return -2 # unexpected ret choice
    
    # else 0<= ret < max_numchoice 
    # wait thread end
    end_sig = 0
    destroy_threads()
    # close the guide window and return the selected event handler
    guide_window[2]()

    # [main will run selected event handler]
    return ret