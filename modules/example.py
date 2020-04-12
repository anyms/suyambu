#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""

from core.module import Module


class SuyambuModule(Module):
    def __init__(self):
        Module.__init__(self)
        self.name = "Example Module"
        self.description = "This is an example Module"
        self.author = ["Jeeva"]
        self.options.add("name", "", "Your name")

    def run(self):
        name = self.options.get("name").upper()
        print("Hello, {}!".format(name))
