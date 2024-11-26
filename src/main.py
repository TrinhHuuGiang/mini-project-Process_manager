'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys

# auto run libraries
from _1_auto_run.guide.auto_guide import guide_auto_run
from _1_auto_run.CRP.auto_CRP import CRP_auto_run

# error code
from error_code import *

'''****************************************************************************
* Code
****************************************************************************'''
#[main]
# exit code:
# (0) normal exit
def main():
    #[add CRP window first]
    
    #run guilde window first
    ret = guide_auto_run()
    while(ret >= 0):
        # check choice returned
        if debug == CommonErrorCode.DEBUG:
            print("return window:",ret)
            input("input anything to contine :)")
        # open choice window
        if ret == 0:
            if(CRP_auto_run()):
                sys.exit(0) # unexpected
        if ret == 1:
            with open("about.txt", "r", encoding="utf-8") as file:
                print("\n\n",file.read())
            input("\n[Press any thing to close]\n")
        else: #>1
            print("[WARN - {}] Unexpected event".format(main.__name__),
              file=sys.stderr)
        ret = guide_auto_run()

    #exit
    sys.exit(0)


if __name__ == "__main__":
    main()
