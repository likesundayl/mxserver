# -*- coding: utf-8 -*-

# @Time    : 2018/1/6 19:48
# @Author  : Terence Wu
# @License : Copyright (c) Terence Wu


def exception_msg(level, exception):
    if level == 'DETAILED':
        import traceback
        msg = traceback.format_exc()
    elif level == 'BASIC':
        msg = repr(exception)
    else:
        msg = str(exception)

    return msg

