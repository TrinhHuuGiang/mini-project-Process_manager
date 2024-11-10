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
# defined libraries
from _3_curses_window.CPU_RAM_PROC.CRP_win import CRPwin #inherit class for CRP window

'''****************************************************************************
* Variable
****************************************************************************'''
w_CRP = None

'''****************************************************************************
* Code
****************************************************************************'''
# [handler for CPU/RAM/PROC window]
# initialize and check size, set color
def init_guide_window():
    global w_CRP
    #init guide window object
    w_CRP = CRPwin()
    #check size
    if(w_CRP.Check_Size()):
        #size invalid
        return -1
    #check color
    w_CRP.Check_color_and_set()
    #test color
    w_CRP.Hello_World()
    #anything ok
    return 0

