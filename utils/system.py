#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 fisherman developers (http://fisherman.lk)
See the file 'LICENSE' for copying permission
"""

import json
import os
import platform
from shutil import get_terminal_size, rmtree
import sys
from time import gmtime, strftime
import math


def is_win():
    """Check if is a Windows system"""
    return platform.system() == "Windows"


def terminal_width():
    """Get available terminal width"""
    return get_terminal_size((80, 20)).columns


def empty_folder(path):
    """Delete a folder content recursively"""
    rmtree(path, ignore_errors=True)


def get_time():
    """Get the current time formatted by HOUR:MINUTE:SECOND"""
    return strftime("%H:%M:%S", gmtime())


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    number_of_list = math.ceil(len(lst)/n)
    for i in range(0, len(lst), number_of_list):
        yield lst[i:i + n]

