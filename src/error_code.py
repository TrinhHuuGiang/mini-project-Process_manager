from enum import Enum

class CommonErrorCode(Enum):
    #[ 0 - 20 ] Common Nontify
    OK = 0
    END_SIG = 1
    NOT_END_SIG = 2
    CHECKED = 3
    NOT_CHECKED = 4
    DEBUG = 5
    NOT_DEBUG = 6


    #[ -20 -> -1 ] special negative signals
    UNKNOWN_ERROR = -1

    #[ -50 -> -21 ] display curses error
    ERROR_INVALID_MIN_SIZE = -21
    ERROR_SIZE_CHANGED = -22


    #[ -100 -> -50] process psutil error code


#debug mode default
debug = CommonErrorCode.DEBUG