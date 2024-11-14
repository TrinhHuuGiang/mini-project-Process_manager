'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys

# handler libraries
from _2_window_handler import CRP_handler

'''****************************************************************************
* Variable
****************************************************************************'''
# list function handle of CRP window
CRP_window = [CRP_handler.init_CRP_window,CRP_handler.getkey_CRPwindow,
              CRP_handler.exit_CRP_window]

'''****************************************************************************
* Code
****************************************************************************'''
# [CRP auto run]
# It will run processing commands step by step:
# - initialize the CRP screen
# - close the CRP window
# return code:
# (-1) window too small
def CRP_auto_run():
    # [guide handler]
    # initialize display process window
    CRP_window[0]()
    
    #else wait use type some thing
    CRP_window[1]()

    #return terminal to re open menu
    CRP_window[2]()
    
    #exit ok
    return 0
