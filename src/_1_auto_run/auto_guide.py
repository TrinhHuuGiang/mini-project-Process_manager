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
res_sig = 1

'''****************************************************************************
* Code
****************************************************************************'''
# [Initialize support threads]
def resize_win():
    global res_sig
    while res_sig:
        guide_handler.resize_guide_window()

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
    global res_sig

    # [guide handler]
    # initialize menu guide window
    max_num_choice = guide_window[0]()
    
    # start create support threads
    thread1 = threading.Thread(target=resize_win)
    thread1.start()

    # runs automatically until the user selects a display window
    ret = guide_window[1]()
    if(ret == -1):
        # wait thread end
        res_sig = 0
        thread1.join()
        # close 'curses' and switch back to the original terminal
        guide_window[2]()
        print("[OK - {}] - Closed".format(guide_auto_run.__name__), file=sys.stderr)
        return -1 # no error, exit
    elif((ret < 0 ) and (ret >= max_num_choice )):
        # wait thread end
        res_sig = 0
        thread1.join()
        # close 'curses' and switch back to the original terminal
        guide_window[2]()
        print("[ERR - {}] - Unexpected event".format(guide_auto_run.__name__), file=sys.stderr)
        return -2 # unexpected ret choice
    
    # else 0<= ret < max_numchoice 
    # wait thread end
    res_sig = 0
    thread1.join()
    # close the guide window and return the selected event handler
    guide_window[2]()

    # [main will run selected event handler]
    return ret