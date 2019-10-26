#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 fisherman developers (http://fisherman.lk)
See the file 'LICENSE' for copying permission
"""

from cmd import Cmd
import sqlite3

from utils.colorify import dim


class Console(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.prompt = "{} > ".format(dim("fisherman"))
        
        
    def do_update_db(self, line):
        conn = sqlite3.connect("fisherman.db")
        c = conn.cursor()
        
        c.close()
        conn.close()
