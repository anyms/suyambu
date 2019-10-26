#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 fisherman developers (http://fisherman.lk)
See the file 'LICENSE' for copying permission
"""

def format_percentage(current, total):
    per = str(round(current/total*100, 1))
    if len(per) == 3:
        return "  {}%".format(per)
    elif len(per) == 4:
        return " {}%".format(per)

    return per


def format_space(s, count):
    return s + (" " * (count - len(s)))
