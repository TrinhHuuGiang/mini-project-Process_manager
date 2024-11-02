'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys

# handler libraries
from window_handler import guide_handler, CRD_handler, CRP_handler, NS_handler

'''****************************************************************************
* Variable
****************************************************************************'''
guide_window = [guide_handler.init_guide_window(),guide_handler.auto_run_guide_window(),
guide_handler.exit_guide_window()]


'''****************************************************************************
* Code
****************************************************************************'''
def main():
    ret = 0
    # [guide handler]
    # initialize and check size
    if(guide_window[0]):
        print("[ERR - {}] - Terminal size too small".format(main.__name__), file=sys.stderr)
        guide_window[2] # close 'curses' and switch back to the original terminal 
        return 1
    # runs automatically until the user selects a display function
    ret = guide_window[1]
    if(ret == -1):
        print("[ERR - {}] - Unexpected error".format(main.__name__), file=sys.stderr)
    elif(ret):
        if(ret == 0): pass
        elif(ret == 1): pass
        elif(ret == 2): pass
    else:
        print("[ERR - {}] - Unexpected event".format(main.__name__), file=sys.stderr)
    # close the guide window and run the selected event handler
    # close the guide window
    guide_window[2]

    # run selected event handler



    #any thing ok
    return 0


if __name__ == "__main__":
    main()
