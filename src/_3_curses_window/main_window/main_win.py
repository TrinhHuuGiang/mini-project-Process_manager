'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
from _3_curses_window.container_class.container import *
'''****************************************************************************
* Variable
****************************************************************************'''
#sub order window
w_order_begin_col = 3
w_order_begin_row = 1
w_order_col = 76
w_order_row = 18
max_num_choice = 3
numerical_order = 0
order_choice = ("- Change color","- Change style","- ON/off border")

#sub instruction window
w_guide_begin_col = 3
w_guide_begin_row = 20
w_guide_col = 76
w_guide_row = 4

'''****************************************************************************
* Code
****************************************************************************'''
class Main_win(Container):
    # Initialize display windows
    def __init__(self):
        # init backwindow
        Container.__init__(self)
        #init sub win
        self.w_order = curses.newwin(w_order_row,w_order_col,w_order_begin_row,w_order_begin_col)
        self.w_guide = curses.newwin(w_guide_row,w_guide_col,w_guide_begin_row,w_guide_begin_col)

        # now add keypad(True) for order and guide window
        self.w_order.keypad(True), self.w_guide.keypad(True)

    #de-init
    def __del__(self):
        Container.__del__(self)
            
    # ______________[interract with window]_____________
    # [add border]
    def Set_border(self):
        self.backwin.box('|','-')
        self.w_order.box('|','-')
        self.w_guide.box('|','-')
        
        #refresh
        self.backwin.refresh()
        self.w_order.refresh()
        self.w_guide.refresh()

    # [order window]
    def update_order(self):
        i = 0
        for item in order_choice:
            if(i == numerical_order):#if current order, highlight it
                self.w_order.addstr(i+1,2,item,curses.A_REVERSE)
            else:
                self.w_order.addstr(i+1,2,item)
            #increase i
            i+=1
        self.w_order.refresh()

    # get numerical order of current order
    def get_order(self):
        return numerical_order

    # using update_order after order_top, down
    # up
    def order_down(self):
        global numerical_order
        numerical_order+=1
        if(numerical_order == max_num_choice):
            numerical_order = 0
    # down
    def order_top(self):
        global numerical_order
        numerical_order-=1
        if(numerical_order < 0):
            numerical_order = max_num_choice - 1

    