'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
'''****************************************************************************
* Variable
****************************************************************************'''
#background window
back_win_max_col = 80
back_win_max_row = 24
#sub order window
w_order_begin_col = 1
w_order_begin_row = 1
w_order_col = 76
w_order_row = 16
#sub instruction window
w_guide_begin_col = 1
w_guide_begin_row = 18
w_guide_col = 76
w_guide_row = 4


'''****************************************************************************
* Code
****************************************************************************'''
class Container:
    # Initialize display windows
    def __init__(self):
        # init main window
        self.backwin = curses.initscr()
        self.w_order = curses.newwin(w_order_row,w_order_col,w_order_begin_row,w_order_begin_col)
        self.w_guide = curses.newwin(w_guide_row,w_guide_col,w_guide_begin_row,w_guide_begin_col)

        #set border and content
        self.__private_content()
        
        #wait
        self.backwin.getkey()

        #end
        self.backwin.endwin()

    # [Should check main window before printing anything]
    def Check_Size(self):
        if(((back_win_max_col)<self.backwin.getmaxy()) and ((back_win_max_row)<self.backwin.getmaxx())):
            return 0 #ok
        return -1 # col or row too little

    def __private_content(self):
        self.backwin.box('|','-')
        self.w_order.box('|','-')
        self.w_guide.box('|','-')
        
        #refresh
        self.backwin.refresh()
        self.w_order.refresh()
        self.w_guide.refresh()
