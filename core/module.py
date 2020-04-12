#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""

import os

from core.options import Options
from utils import log
from utils.colorify import bold, blue
from libs.table import Table


class Module:
    def __init__(self):
        self.name = "-"
        self.description = "-"
        self.author = []
        self.license = "MIT"

        self.options = Options()
        self.plugins = []
        self.plugin_strings = []

        for root, dirs, files in os.walk("plugins"):
            for f in files:
                rt = "/".join(root.split("/")[1:])
                if rt.strip():
                    path = "{}/{}".format(rt, f)
                else:
                    path = "{}".format(f)
                if path.endswith(".py"):
                    ms = ".".join(path.split(".")[:-1])
                    self.plugin_strings.append(ms)

    def setup(self):
        return True

    def do_run(self, line):
        """run the module"""
        for plugin in self.plugins:
            try:
                plugin.run()
            except Exception as e:
                log.error("A plugin failed: {}".format(e))
        if self.plugins:
            log.info("Plugins execution done")
        try:
            self.run()
        except Exception as e:
            log.error("Module failed: {}".format(e))
        log.info("Done.")

    def do_options(self, line):
        """show available options"""
        print("\nModule Options:\n")
        options = self.options.to_dict()
        if options:
            table = Table()
            values = []
            descriptions = []
            for op in options.keys():
                values.append(options[op]["value"])
                descriptions.append(options[op]["description"])
            
            table.add("Options", list(options.keys()))
            table.add("Default Values", values)
            table.add("Description", descriptions)

            print(table)
        
        print(self.description)
        print()

        if self.plugins:
            print("\nPlugin(s) Options:\n")
            for plugin in self.plugins:
                print(blue("* {}  =>\n".format(plugin.name)))
                plugin.do_options("")

    def do_set(self, line):
        """set module or plugin options"""
        nodes = line.split(" ")
        try:
            if nodes[0].upper() == "PLUGIN":
                for plugin in self.plugins:
                    plugin.options.set(nodes[1], nodes[2])
                log.info("{} => {}".format(nodes[1], nodes[2]))
            else:
                self.options.set(nodes[0], nodes[1])
                log.info("{} => {}".format(nodes[0], nodes[1]))
        except IndexError:
            log.error("Insufficient arguments")

    def complete_set(self, text, line, begidx, endidx):
        options = self.options.to_dict()

        nodes = line.split(" ")
        mline = self.autocomp(line, len(nodes) - 1)
        offs = len(mline) - len(text)
        comps = []
        if len(nodes) <= 2:
            comps = list(options.keys())
            if self.plugins:
                comps += ["PLUGIN"]
            if text.isupper():
                comps = [s.upper() for s in comps]
            else:
                comps = [s.lower() for s in comps]
        elif len(nodes) <= 3:
            node = line.split(" ")[1]
            if node.upper() == "PLUGIN":
                comps = []
                for plugin in self.plugins:
                    comps += list(plugin.options.to_dict().keys())
                if text.isupper():
                    comps = [s.upper() for s in comps]
                else:
                    comps = [s.lower() for s in comps]
        elif len(nodes) <= 4:
            pass
        
        return [s[offs:] for s in comps if s.startswith(mline)]

    def autocomp(self, line, num):
        mline = line.partition(" ")[2]
        for i in range(num-1):
            mline = mline.partition(" ")[2]

        return mline

    def do_load(self, line):
        """load a plugin into a module"""
        try:
            plug = __import__("plugins.{}".format(line.replace("/", ".")), fromlist=["SuyambuPlugin"]).SuyambuPlugin()
            if plug.setup():
                self.plugins.append(plug)
            else:
                log.error("Unable to load '{}' setup failed".format(line))
        except AttributeError:
            log.error("It is not a Suyambu plugin")

    def complete_load(self, text, line, begidx, endidx):
        nodes = line.split(" ")
        mline = self.autocomp(line, len(nodes) - 1)
        offs = len(mline) - len(text)
        comps = []
        if len(nodes) <= 2:
            comps = self.plugin_strings
        return [s[offs:] for s in comps if s.startswith(mline)]

    def log_info(self, s):
        log.info(s)
    
    def log_error(self, s):
        log.error(s)
    
    def log_warn(self, s):
        log.warn(s)
    
    def log_success(self, s):
        log.success(s)
    


class Plugin:
    def __init__(self):
        self.name = "-"
        self.description = "-"
        self.author = []
        self.license = "MIT"

        self.options = Options()

    def setup(self):
        return True

    def run(self):
        pass

    def do_options(self, line):
        options = self.options.to_dict()
        if options:
            table = Table()
            values = []
            descriptions = []
            for op in options.keys():
                values.append(options[op]["value"])
                descriptions.append(options[op]["description"])
            
            table.add("Options", list(options.keys()))
            table.add("Default Values", values)
            table.add("Description", descriptions)

            print(table)
        print(self.description)
        print()

    def log_info(self, s):
        log.info(s)
    
    def log_error(self, s):
        log.error(s)
    
    def log_warn(self, s):
        log.warn(s)
    
    def log_success(self, s):
        log.success(s)
