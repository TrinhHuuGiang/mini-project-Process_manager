'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys

# defined libraries
from _3_curses_window.main_window.main_win import (Container, back_win_max_row,
back_win_max_col)

'''****************************************************************************
* Variable
****************************************************************************'''


'''****************************************************************************
* Code
****************************************************************************'''
if __name__ == "__main__":
    # initialize object guide window: background, orderlist, guide to use
    Guide_window = Container()
    if(Guide_window.Check_Size()):
        del Guide_window
        # print to stderr (terminal)
        print("Error: max-row {}, max-col {}".format(back_win_max_row, back_win_max_col),
        file=sys.stderr)
    else:
        del Guide_window
        print("OK", file=sys.stderr)
    