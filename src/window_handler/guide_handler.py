'''
Include handler functions for each window:
    + Guide <==
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
# common libraries
import sys

# defined libraries
from curses_window.main_window.main_win import Container #main class for guide window)


'''****************************************************************************
* Variable
****************************************************************************'''
w_guide = None

'''****************************************************************************
* Code
****************************************************************************'''
# [handler for guide window]
# initialize and check size
def init_guide_window():
    global w_guide
    w_guide = Container()
    if(w_guide.Check_Size()):
        #size invalid
        return -1
    else:
        #suitable size
        return 0

# auto handle
def auto_run_guide_window():
    global w_guide
    # draw border
    w_guide.Set_border()
    
    # update list order
    w_guide.update_order()

    # wait user then update or execute or quit 'q'
    temp_input = 'nothing'
    temp_choice= -1
    while (temp_input != 'q'):
        temp_input = w_guide.w_order.getkey()
        if(temp_input == 'w'):
            w_guide.order_top()
            # update list order
            w_guide.update_order()
        elif(temp_input == 's'):
            w_guide.order_down()
            # update list order
            w_guide.update_order()
        elif(temp_input == '\n'):
            return w_guide.get_order()

    #if input == q
    return -1 # quit signal

# end
def exit_guide_window():
    global w_guide
    del w_guide #free completely window curses and switch back to the original terminal 
    print("[OK - {}] closed the guide window".format(exit_guide_window.__name__),
    file=sys.stderr)
    # no return
