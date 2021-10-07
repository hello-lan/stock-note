# -*- coding: utf-8 -*-


def none_to_zero(value):
    return 0.0 if value is None else value


none_to_zeros = none_to_zero


def format_thousand_separator(value):
    """ 用千位分隔符格式化数字
    """
    if isinstance(value, int) or isinstance(value,float):
        return "{:,}".format(value)
    else:
        return value
