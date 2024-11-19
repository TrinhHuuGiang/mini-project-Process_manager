from enum import Enum

class ErrorCode(Enum):
    #Common Nontify
    OK = 0
    END_SIG = 1
    NOT_END_SIG = 2
    CHECKED = 3
    NOT_CHECKED = 4
    DEBUG = 5
    NOT_DEBUG = 6
    #Error
    ERROR_INVALID_MIN_SIZE = -1
    ERROR_SIZE_CHANGED = -2

#debug mode default
debug = ErrorCode.DEBUG
