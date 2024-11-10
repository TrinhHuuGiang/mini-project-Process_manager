'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys

# handler libraries
from _2_window_handler import guide_handler
from _3_curses_window.main_window.main_win import max_num_choice

'''****************************************************************************
* Variable
****************************************************************************'''
# list function handle of guide window
guide_window = [guide_handler.init_guide_window,guide_handler.update_menu_list_and_get_choice,
guide_handler.exit_guide_window]

'''****************************************************************************
* Code
****************************************************************************'''
# [guide auto run]
# It will run processing commands step by step:
# - initialize the screen
# - run the menu to take selections from the user
# - close the order window and return the order code.
# return code:
# (-1) window too small; (-2) user want exit program
# 0,1,2,3... is code of other windows
def guide_auto_run():
    ret = 0
    # [guide handler]
    # initialize and check size
    if(guide_window[0]()):
        guide_window[2]() # close 'curses' and switch back to the original terminal 
        print("[ERR - {}] - Terminal size too small".format(guide_auto_run.__name__), file=sys.stderr)
        return -1
    
    # runs automatically until the user selects a display window
    ret = guide_window[1]()
    if(ret == -1):
        # close 'curses' and switch back to the original terminal
        guide_window[2]()
        print("[OK - {}] - Closed".format(guide_auto_run.__name__), file=sys.stderr)
        return -2 # no error, exit
    elif((ret < 0 ) and (ret >= max_num_choice )):
        print("[ERR - {}] - Unexpected event".format(guide_auto_run.__name__), file=sys.stderr)
    
    # else 0<= ret < max_numchoice 
    # close the guide window and return the selected event handler
    guide_window[2]()

    # [main will run selected event handler]
    return ret