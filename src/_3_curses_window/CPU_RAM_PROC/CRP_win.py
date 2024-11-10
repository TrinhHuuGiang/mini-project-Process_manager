'''****************************************************************************
* Definitions
****************************************************************************'''
import curses
from _3_curses_window.container_class.container import *

'''****************************************************************************
* Variable
****************************************************************************'''
# inherit the 'Container' class
class CRPwin(Container):
    # Initialize display windows
    def __init__(self):
        Container.__init__(self)

    def __del__(self):
        Container.__del__(self)

    # ______________[interract with window]_____________
    # [add border]
    def Set_border(self):
        self.backwin.box('|','-')
        
        #refresh
        self.backwin.refresh()
