'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys

# handler libraries
from _2_display_module import guide_handler, CRD_handler, CRP_handler, NS_handler
from _3_display_component.main_window.main_win import max_num_choice

'''****************************************************************************
* Variable
****************************************************************************'''
# list function handle of guide window
guide_window = [guide_handler.init_guide_window,guide_handler.auto_run_guide_window,
guide_handler.exit_guide_window]

# lisr funtion handle for other window
# depend on 'ret'


'''****************************************************************************
* Code
****************************************************************************'''
def main():
    ret = 0
    # [guide handler]
    # initialize and check size
    if(guide_window[0]()):
        guide_window[2]() # close 'curses' and switch back to the original terminal 
        print("[ERR - {}] - Terminal size too small".format(main.__name__), file=sys.stderr)
        return 1
    # runs automatically until the user selects a display function
    ret = guide_window[1]()

    if(ret == -1):
        # close 'curses' and switch back to the original terminal
        guide_window[2]()
        print("[OK - {}] - Closed".format(main.__name__), file=sys.stderr)
        return 0 # no error, exit
    elif((ret < 0 ) and (ret >= max_num_choice )):
        print("[ERR - {}] - Unexpected event".format(main.__name__), file=sys.stderr)
    
    # close the guide window and run the selected event handler
    # close the guide window
    guide_window[2]()

    # [run selected event handler]
    print("next display: {}".format(ret))


    #any thing ok
    return 0


if __name__ == "__main__":
    main()
