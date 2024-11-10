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

# [pseudo color or style]
# only use when call Container.Check_color_and_set()
COS = [
    "red black or BOLD", # for alert
    "magenta black or DIM", # for not important
    "blue black or UNDERLINE", # for suggest
    "yellow black or REVERSE", # for highlight
    "green black or STANDOUT", # for highlight
    "cyan black or BLINK"] # for notification

'''****************************************************************************
* Code
****************************************************************************'''
class Container:
    # Initialize display windows
    def __init__(self):
        # init main window
        self.backwin = curses.initscr()
        # add cbreak (auto enter), keypad(true)(convert special key to curses key), noecho (hide input)
        # :) i don't know why initscr not auto do it
        curses.cbreak(), curses.noecho()

        #init sub win
        self.w_order = curses.newwin(w_order_row,w_order_col,w_order_begin_row,w_order_begin_col)
        self.w_guide = curses.newwin(w_guide_row,w_guide_col,w_guide_begin_row,w_guide_begin_col)

        # now add keypad(True)
        self.backwin.keypad(True), self.w_order.keypad(True), self.w_guide.keypad(True)

    #de-init
    def __del__(self):
        curses.endwin()

    # ______________[checking resource]_____________
    # [Should check size main window before printing anything]
    def Check_Size(self):
        if ((back_win_max_col < self.backwin.getmaxyx()[1]) and (back_win_max_row < self.backwin.getmaxyx()[0])):
            return 0 #ok
        return -1 # col or row too little

    # [check color and set color]
    # if you want color, call it
    # if color not avalable -> change it by another style
    # basic color: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    # color pair index start is 1
    # basic style: A_BLINK, A_BOLD, A_DIM, A_REVERSE, A_STANDOUT, A_UNDERLINE,...
    def Check_color_and_set(self):
        global COS
        curses.start_color()#set up default curses color
        if not curses.has_colors():
            COS = [curses.A_BOLD,curses.A_DIM,curses.A_UNDERLINE,
                   curses.A_REVERSE, curses.A_STANDOUT, curses.A_BLINK]
        else:# have color
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
            COS = [curses.color_pair(1), curses.color_pair(5), curses.color_pair(4),
                   curses.color_pair(3), curses.color_pair(2), curses.color_pair(6)]
            
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
    
    #print hello
    def Hello_World(self):
        self.backwin.addstr(19, back_win_max_col//2 -15  ,"hello",COS[0])
        self.backwin.addstr(19, back_win_max_col//2 -10    ,"hello",COS[1])
        self.backwin.addstr(19, back_win_max_col//2 -5      ,"hello",COS[2])
        self.backwin.addstr(19, back_win_max_col//2          ,"hello",COS[3])
        self.backwin.addstr(19, back_win_max_col//2 +5    ,"hello",COS[4])
        self.backwin.addstr(19, back_win_max_col//2 +10,"hello",COS[5])
        self.backwin.refresh()

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

    