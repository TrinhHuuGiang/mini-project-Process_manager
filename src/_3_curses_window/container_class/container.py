'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
'''****************************************************************************
* Variable
****************************************************************************'''

'''****************************************************************************
* Code
****************************************************************************'''
class Container:
    #background window
    back_win_min_col = 80
    back_win_min_row = 24

    # [pseudo color or style]
    # only use when call Container.Check_color_and_set()
    COS = None
    # [
    # "red black or BOLD", # for alert
    # "magenta black or DIM", # for not important or guide
    # "blue black or UNDERLINE", # for suggest
    # "yellow black or REVERSE", # for highlight
    # "green black or STANDOUT", # for highlight
    # "cyan black or BLINK"] # for notification

    # [Initialize display windows]
    def __init__(self):
        # init main window
        self.backwin = curses.initscr()
        # add cbreak (auto enter), keypad(true)(convert special key to curses key), noecho (hide input)
        # :) i don't know why initscr not auto do it
        # cbreak, noecho only set once
        curses.cbreak(), curses.noecho()
        # hide cursor
        curses.curs_set(0)
        # now add keypad(True), this function have to set for every new window
        self.backwin.keypad(True)

    #de-init
    def __del__(self):
        curses.endwin()

    # ______________[checking resource]_____________
    # [Should check size main window before printing anything]
    def Check_Size(self):
        if ((Container.back_win_min_col < self.backwin.getmaxyx()[1]) and 
            (Container.back_win_min_row < self.backwin.getmaxyx()[0])):
            return 0 #ok
        return -1 # col or row too little

    # [check color and set color]
    # if you want color, call it
    # if color not avalable -> change it by another style then update into list COS[]
    # defaut basic color: 0:black, 1:red, 2:green, 3:yellow, 4:blue, 5:magenta, 6:cyan, and 7:white
    # but real test on 'bash' on linux we see that:
    #  0: black, 1: red, 5: green, 4: yellow, 3: blue, 2: magneta, 6: cyan
    # color pair index start is 1
    # basic style: A_BLINK, A_BOLD, A_DIM, A_REVERSE, A_STANDOUT, A_UNDERLINE,...
    def Check_color_and_set(self):
        curses.start_color()#set up default curses color
        if not curses.has_colors():
            Container.COS = [curses.A_BOLD,curses.A_DIM,curses.A_UNDERLINE,
                   curses.A_REVERSE, curses.A_STANDOUT, curses.A_BLINK]
        else:# have color
            curses.init_pair(1, 1, 0)#red
            curses.init_pair(2, 2, 0)#mag
            curses.init_pair(3, 3, 0)#blue
            curses.init_pair(4, 4, 0)#yellow
            curses.init_pair(5, 5, 0)#green
            curses.init_pair(6, 6, 0)#cyan
            Container.COS = [curses.color_pair(1), curses.color_pair(5), curses.color_pair(4),
                   curses.color_pair(3), curses.color_pair(2), curses.color_pair(6)]
            
    # ______________[interract with window]_____________
    
    #[print hello to test color]
    #must Check_color_and_set() before use this function
    def Hello_World(self):
        self.backwin.addstr(19, Container.back_win_min_col//2 -15 ,"Qquit",COS[0])
        self.backwin.addstr(19, Container.back_win_min_col//2 -10 ,"_____",COS[1])
        self.backwin.addstr(19, Container.back_win_min_col//2 -5  ,"hello",COS[2])
        self.backwin.addstr(19, Container.back_win_min_col//2     ,"hello",COS[3])
        self.backwin.addstr(19, Container.back_win_min_col//2 +5  ,"_____",COS[4])
        self.backwin.addstr(19, Container.back_win_min_col//2 +10 ,"Qquit",COS[5])
        self.backwin.refresh()
