'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
from _3_display_component.container_class.container import Container

'''****************************************************************************
* Constants
****************************************************************************'''
max_num_choice = 3
'''****************************************************************************
* Code
****************************************************************************'''
class Main_win(Container):
    # Initialize display windows
    def __init__(self):
        #Variable and constant
        #sub order window
        self.w_order_begin_col = None; self.w_order_begin_row = None
        self.w_order_col = None; self.w_order_row = None
        self.numerical_order = 0
        self.order_choice = ("CPU - RAM - PROCESS","- Change style","- ON/off border")
        #sub instruction window
        self.w_guide_begin_col = None; self.w_guide_begin_row = None
        self.w_guide_col = None; self.w_guide_row = None

        # minsize for all window
        self.w_order_mincol = 5; self.w_order_minrow = 5
        self.w_guide_mincol = 5; self.w_guide_minrow = 5
        self.w_back_mincol= self.w_order_mincol+self.w_guide_mincol
        self.w_back_minrow= self.w_order_minrow+self.w_guide_minrow 

        # window variable
        self.w_order = None; self.w_guide = None
        # init backwindow
        Container.__init__(self)
        # calculate sub win size
        self.cal_size_sub_window()
        # init sub window
        self.w_order = curses.newwin(self.w_order_row,self.w_order_col,
                                     self.w_order_begin_row,self.w_order_begin_col)
        self.w_guide = curses.newwin(self.w_guide_row,self.w_guide_col,
                                     self.w_guide_begin_row,self.w_guide_begin_col)

        # now add keypad(True)
        self.w_order.keypad(True), self.w_guide.keypad(True)

        # set border
        self.Set_border()

    # De-init
    def __del__(self):
        Container.__del__(self)
            
    # ______________[interract with window]_____________
    # *****[A. calculate and re-set size window]*****
    def cal_size_sub_window(self):
        #order window
        self.w_order_begin_col = self.back_win_col * 10 // 100
        self.w_order_begin_row = self.back_win_row * 10 // 100
        self.w_order_col = self.back_win_col * 80 // 100
        self.w_order_row = self.back_win_row * 50 // 100

        #guide window
        self.w_guide_begin_col = self.back_win_col * 10 // 100
        self.w_guide_begin_row = self.back_win_row * 60 // 100
        self.w_guide_col = self.w_order_col
        self.w_guide_row = self.back_win_row * 30 // 100

        #fix size if invalid, min 5
        if(self.w_order_col < self.w_order_mincol): self.w_order_col = self.w_order_mincol
        if(self.w_order_row < self.w_order_minrow): self.w_order_row = self.w_order_minrow
        if(self.w_guide_col < self.w_guide_mincol): self.w_guide_col = self.w_guide_mincol
        if(self.w_guide_row < self.w_guide_minrow): self.w_guide_row = self.w_guide_minrow

    # clear all window
    def clear_all_window(self):
        self.backwin.clear()
        self.w_order.clear()
        self.w_guide.clear()


    #update size and move coordinate after calculate
    def update_size_sub_window(self):
        # update size
        self.w_order.resize(self.w_order_row,self.w_order_col)
        self.w_guide.resize(self.w_guide_row,self.w_guide_col)
        # update coordinate
        self.w_order.mvwin(self.w_order_begin_row,self.w_order_begin_col)
        self.w_guide.mvwin(self.w_guide_begin_row,self.w_guide_begin_col)

    # *****[B. add border window]*****
    def Set_border(self):
        self.backwin.box('|','-')
        self.w_order.box('|','-')
        self.w_guide.box('|','-')
        
        #refresh
        self.backwin.refresh()
        self.w_order.refresh()
        self.w_guide.refresh()

    # *****[C. order menu for order window]*****
    def update_order(self):
        i = 0
        for item in self.order_choice:
            if(i == self.numerical_order):#if current order, highlight it
                self.w_order.addstr(i+1,2,item,curses.A_REVERSE)
            else:
                self.w_order.addstr(i+1,2,item)
            #increase i
            i+=1
        self.w_order.refresh()

    # get numerical order of current order
    def get_order(self):
        return self.numerical_order

    # using update_order after order_top, down
    # up
    def order_down(self):
        self.numerical_order+=1
        if(self.numerical_order == max_num_choice):
            self.numerical_order = 0
    # down
    def order_top(self):
        self.numerical_order-=1
        if(self.numerical_order < 0):
            self.numerical_order = max_num_choice - 1

    