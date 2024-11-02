'''
Include handler functions for each window:
    + Guide
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
# defined libraries
from curses_window.main_window.main_win import (Container, back_win_max_row,
back_win_max_col)#main class for guide window


'''****************************************************************************
* Variable
****************************************************************************'''


'''****************************************************************************
* Code
****************************************************************************'''
# [handler for guide window]

# [handler for CPU/RAM/DISK window]

# [handler for CPU/RAM/PROC window]

# [handler for NET/SERVICE window]

