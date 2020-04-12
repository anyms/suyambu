#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""

import os

from core.module import Plugin


class SuyambuPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.name = "Ngrok"
        self.description = "Use ngrok service to forward local port (Only supports HTTP traffic)"
        self.author = ["Jeeva"]
        self.options.add("lport", "", "Local port to forward")

        self.ngrok = None

    def setup(self):
        try:
            from pyngrok import ngrok
            self.ngrok = ngrok
        except:
            ask = self.log_info("pyngrok module not found, would you like to install? (Y/n) ").lower()
            if ask in ["y", "yes"]:
                return os.system("sudo pip3 install pyngrok") == 0
            return False
        return True

    def run(self):
        port = int(self.options.get("lport"))
        self.log_info("Initiating ngrok tunner...")
        self.ngrok.connect(port)
        tunnels = self.ngrok.get_tunnels()
        self.log_success("Ngrok public URL: {}".format(tunnels[0].public_url))
