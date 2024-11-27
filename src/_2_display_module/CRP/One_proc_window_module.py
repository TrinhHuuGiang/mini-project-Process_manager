'''
Include handler functions for each window:
    + Menu/Guide
    + CPU/RAM/PROC (1 process information) <==
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
import time
import threading #mutex

# defined libraries
from _3_display_component.CRP.One_proc_win_component import CRPwin #inherit class for one process window

# error code
from error_code import *
'''****************************************************************************
* Variable
****************************************************************************'''

'''****************************************************************************
* Code
****************************************************************************'''
#renew global variable if recall this window
def renew_global_variable():
    pass

# [handler for one process window]
# initialize and check size, set color, set box
def init_CRP_window():
    pass

# wait to get key
def getkey_CRPwindow():
    pass

# end
def exit_CRP_window():
    pass

# ___________[Thread_Function]___________
# Call these support function after init window
# A. Resize window (support)
# check resize or size not invalid
def check_size_valid():
    pass

# B. push content to background (thread) (T1)
def push_to_screen():
    pass

# E. Release data total resource will display to buffer (thread) (T4.1+T4.2)
def update_total_resource():
    pass