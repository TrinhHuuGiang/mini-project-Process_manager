'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
from _3_display_component.container_class.container import Container

'''****************************************************************************
* Variable
****************************************************************************'''
# inherit the 'Container' class
class CRPwin(Container):
    # Initialize display windows
    def __init__(self):
        #Variable and constant
        ##[process window]
        #include: name, Pid, %CPU, %RAM, Status, time using
        self.w_proc_begin_col = None; self.w_proc_begin_row = None
        self.w_proc_col = None; self.w_proc_row = None

        #total window
        self.w_total_begin_col = None; self.w_total_begin_row = None
        self.w_total_col = None; self.w_total_row = None

        #guide window
        self.w_guide_begin_col = None; self.w_guide_begin_row = None
        self.w_guide_col = None; self.w_guide_row = None

        # window variable
        self.w_proc = None; self.w_total = None; self.w_guide = None

        # init backwindow
        Container.__init__(self)

        # calculate sub win size
        self.cal_size_sub_window()

        # init sub window
        self.w_proc = curses.newwin(self.w_proc_row,self.w_proc_col,
                                     self.w_proc_begin_row,self.w_proc_begin_col)
        self.w_total = curses.newwin(self.w_total_row,self.w_total_col,
                                     self.w_total_begin_row,self.w_total_begin_col)
        self.w_guide = curses.newwin(self.w_guide_row,self.w_guide_col,
                                     self.w_guide_begin_row,self.w_guide_begin_col)
        
        # now add keypad(True)
        self.w_proc.keypad(True); self.w_proc.keypad(True); self.w_guide.keypad(True)

        # add no delay for using getch()
        self.w_proc.nodelay(True); self.w_proc.nodelay(True); self.w_guide.nodelay(True)

    def __del__(self):
        Container.__del__(self)



    '''_______________[interract with window]___________'''
    # [A. calculate and re-set size window]
    def cal_size_sub_window(self):
        # row: 100% = 10% top border + 50% menu + 10% free space + 20% guide + 10% bottom border (guard)
        # tips: increase % bottom border for 
        # reduce the overflow rate (error) due to not having time to recalculate

        #proc window
        self.w_proc_begin_col = self.back_win_col * 10 // 100
        self.w_proc_begin_row = self.back_win_row * 10 // 100
        self.w_proc_col = self.back_win_col * 80 // 100 #> 60block
        self.w_proc_row = self.back_win_row * 55 // 100

        #guide window
        self.w_guide_begin_col = self.back_win_col * 10 // 100
        self.w_guide_begin_row = self.back_win_row * 70 // 100
        self.w_guide_col = self.back_win_col * 35 // 100 #>25block
        self.w_guide_row = self.back_win_row * 20 // 100

        #total window
        self.w_total_begin_col = self.back_win_col * 50 // 100
        self.w_total_begin_row = self.back_win_row * 70 // 100
        self.w_total_col = self.back_win_col * 40 // 100 # >30 block
        self.w_total_row = self.back_win_row * 20 // 100

    # clear all window
    def clear_all_window(self):
        self.backwin.clear()
        self.w_proc.clear()
        self.w_total.clear()
        self.w_guide.clear()


    #demo proc
    def update_proc_content(self):
        # renew border
        self.w_proc.box('|','-')
        #add content
        self.w_proc.addstr(0,1,"|  PID  |     NAME     | CPU |  MEM  |  STATUS  |    TIME    |",
                           curses.A_BOLD)
        # noutrefresh display
        self.w_proc.noutrefresh()


    #demo total
    def update_total_content(self):
        self.w_total.addstr(1,1,"PID:     |CPU:    |RAM:    ")
        self.w_total.addstr(2,1,"Run:     |Sle:    |USE:    ")

        # renew border
        self.w_total.box('|','-')
        # add name
        self.w_total.addstr(0,1,"[Total]", self.COS[2])
        # noutrefresh display
        self.w_total.noutrefresh()


    #[.static window display]
    #[C. guide users window]
    def update_guide(self):
        self.w_guide.addstr(1,1,"W-up   |S-down")
        self.w_guide.addstr(2,1,"Q-quit |Enter-select")

        # renew border
        self.w_guide.box('|','-')
        # add name
        self.w_guide.addstr(0,1,"[How to use]", self.COS[1])
        # noutrefresh display
        self.w_guide.noutrefresh()

    #[D. background]
    def update_background(self):
        # renew border
        self.w_guide.box('|','-')
        #add name
        self.backwin.addstr(0,1,"[Process Manager]",self.COS[4])
        #noutrefresh to apply new change
        self.backwin.noutrefresh()
