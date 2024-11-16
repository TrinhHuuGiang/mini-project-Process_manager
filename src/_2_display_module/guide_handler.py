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
from _3_display_component.main_window.main_win import Main_win #main class for guide window

'''****************************************************************************
* Variable
****************************************************************************'''
# window
w_guide = None

'''****************************************************************************
* Code
****************************************************************************'''
# [handler for guide window]
# initialize and check size, set color, set box
def init_guide_window():
    global w_guide
    #init guide window object
    w_guide = Main_win()
    #test color
    w_guide.Hello_World()

# auto handle manu
# -1: quit| 0,1,2,... is order choice
def update_menu_list_and_get_choice():
    global w_guide
    
    # update list order
    w_guide.update_order()

    # wait user then update or execute or quit 'q'
    temp_input = 'nothing'
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


# ___________[Thread_Function]___________
# Call these support function after init window
# A. Resize window
def resize_guide_window():
    global w_guide
    # save old background size
    back_col = w_guide.back_win_col
    back_row = w_guide.back_win_row
    # get background size
    w_guide.get_backwin_size()
    if((back_col == w_guide.back_win_col) and
       (back_row == w_guide.back_win_row)):
        return #size not change

    # else calculate size sub windows
    w_guide.cal_size_sub_window()

    # clear, resize and reset border
    w_guide.clear_all_window()
    w_guide.update_size_sub_window()
    w_guide.Set_border()
