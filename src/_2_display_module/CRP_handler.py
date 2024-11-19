'''
Include handler functions for each window:
    + Guide
    + CPU/RAM/DISK
    + CPU/RAM/PROC <==
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
import curses

# defined libraries
from _3_display_component.CPU_RAM_PROC.CRP_win import CRPwin #inherit class for CRP window

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''
w_CRP = None

'''****************************************************************************
* Code
****************************************************************************'''
# [handler for CPU/RAM/PROC window]
# initialize and check size, set color, set box
def init_CRP_window():
    global w_CRP
    #init guide window object
    w_CRP = CRPwin()

# wait to get key
def getkey_CRPwindow():
    global w_CRP
    w_CRP.clear_all_window()
    w_CRP.update_background()
    w_CRP.update_guide();w_CRP.update_proc_content()
    w_CRP.update_total_content()
    curses.doupdate()
    # get an temp input to end window :)
    temp_input = -1
    while (temp_input == -1):
        # then check buffer input
        temp_input = w_CRP.backwin.getch()


# end
def exit_CRP_window():
    global w_CRP
    del w_CRP #free completely window curses and switch back to the original terminal 
    if debug == ErrorCode.DEBUG:
        print("[OK - {}] closed the CRP window".format(exit_CRP_window.__name__),
              file=sys.stderr)
    # no return