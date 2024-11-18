'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys

# auto run libraries
from _1_auto_run.auto_guide import guide_auto_run
from _1_auto_run.auto_CRP import CRP_auto_run

'''****************************************************************************
* Variable
****************************************************************************'''
#[main]
# exit code:
# (0) normal exit
def main():
    #[add CRP window first]
    
    #run guilde window first
    ret = guide_auto_run()
    while(ret >= 0):
        # open another window
        print("return window:",ret)
        input("input anything to contine :)")
        if ret == 0:
            if(CRP_auto_run()):
                sys.exit(0) # unexpected
        if ret == 1:
            pass#open auto CRD (CPU RAM DISK)
        if ret == 2:
            pass#open auto NS  (NET SERVICE)
        if ret == 3:
            with open("about.txt", "r", encoding="utf-8") as file:
                print("\n\n",file.read())
            input("\n[Press any thing to close]\n")
        ret = guide_auto_run()

    #exit
    sys.exit(0)

'''****************************************************************************
* Code
****************************************************************************'''
if __name__ == "__main__":
    main()
