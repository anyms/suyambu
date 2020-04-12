#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""

from core.cmd import Cmd
import sqlite3
import os

try:
    import readline
except:
    readline = None

from utils.colorify import green, underline
from utils import log


class Console(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        self.histfile = os.path.expanduser('~/.suyambu_history')
        self.histfile_size = 1000
        self.prompt = "{} > ".format(underline(green("suyambu")))

    def preloop(self):
        if readline and os.path.exists(self.histfile):
            readline.read_history_file(self.histfile)

    def postloop(self):
        if readline:
            readline.set_history_length(self.histfile_size)
            readline.write_history_file(self.histfile)

    def do_db(self, line):
        """db <operation>"""
        conn = sqlite3.connect("suyambu.db")
        c = conn.cursor()
        
        c.close()
        conn.close()

    def do_exit(self, line):
        """quit out of suyambu"""
        return True

    def default(self, line):
        log.info("Exec: {}\n".format(line))
        os.system(line)
