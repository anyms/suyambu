#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""

from core.module import Plugin


class SuyambuPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.name = "Example Plugin"
        self.description = "This is an example Plugin"
        self.author = ["Jeeva"]
        self.options.add("name", "", "Your name")

    def run(self):
        name = self.options.get("name")
        print("Hello, {}!".format(name))
