# -*- coding: utf-8 -*-

# @Time    : 2018/1/6 19:48
# @Author  : Terence Wu
# @License : Copyright (c) Terence Wu
from config import EXCEPTION_MSG_LEVEL


def exception_msg(exception):
    if EXCEPTION_MSG_LEVEL == 'DETAILED':
        import traceback
        msg = traceback.format_exc()
    elif EXCEPTION_MSG_LEVEL == 'BASIC':
        msg = repr(exception)
    else:
        msg = str(exception)

    return msg

