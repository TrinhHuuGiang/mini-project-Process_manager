"""
Process Manager: A program to manage and monitor system processes.
Copyright (C) 2024  Giang Trinh, VuongNQ, and the development team.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


'''****************************************************************************
* Definitions
****************************************************************************'''
# common libraries
import sys
import os

# auto run libraries
from _1_auto_run.auto_menu import menu_auto_run
from _1_auto_run.auto_CRP import CRP_auto_run

# error code
from error_code import *

'''****************************************************************************
* Code
****************************************************************************'''
#[main]
def main():
    # init CRP_window first
    ret_CRP = CRP_auto_run()
    if debug == CommonErrorCode.DEBUG:
        print("[Note - {}] CRP return:".format(main.__name__),ret_CRP)
        input("input anything to contine.")
    # if any negative signal -> close app
    if ret_CRP < 0:
        sys.exit(0)

    # [if CRP return 0 - open menu]
    ret_menu = 0
    while(ret_menu >= 0):
        #run menu window first
        ret_menu = menu_auto_run()
        # check choice returned
        if debug == CommonErrorCode.DEBUG:
            print("[Note - {}] menu return window:".format(main.__name__),ret_menu)
            input("input anything to contine.")

        # open processes window
        if ret_menu == 0:
            ret_CRP = CRP_auto_run()
            if debug == CommonErrorCode.DEBUG:
                print("[Note - {}] CRP return:".format(main.__name__),ret_CRP)
                input("input anything to contine.")
            # if any negative signal -> close app
            if ret_CRP < 0:
                sys.exit(0)

        # open about us window
        elif ret_menu == 1:
            # clear screen and print "about us"
            os.system("clear")
            # print
            current_dir = os.path.dirname(__file__)  # get current folder path
            file_path = os.path.join(current_dir, "about.txt") # get file text in this folder
            with open(file_path, "r", encoding="utf-8") as file: # print file
                print("\n\n",file.read(),file=sys.stderr)
            # then stop to wait user react
            input()
            
        # else menu return event does not exist
        elif ret_menu > 1:
            print("[WARN - {}] Unexpected event".format(main.__name__),
              file=sys.stderr)

    #exit
    sys.exit(0)


if __name__ == "__main__":
    main()
