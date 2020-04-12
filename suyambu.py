#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file "LICENSE" for copying permission
"""

import math
import sys, os

from core.console import Console
from libs.argparse import ArgParse
from utils import system
from utils import log
from utils.colorify import red, green, underline, yellow


class Suyambu(Console):
    def __init__(self):
        Console.__init__(self)
        self.parser = self.parse_arguments()
        self.args = self.parser.parse()
        self.module = {
            "name": None,
            "commands": [],
            "instance": None
        }
        self.modules_string = []

        for root, dirs, files in os.walk("modules"):
            for f in files:
                rt = "/".join(root.split("/")[1:])
                if rt.strip():
                    path = "{}/{}".format(rt, f)
                else:
                    path = "{}".format(f)
                if path.endswith(".py"):
                    ms = ".".join(path.split(".")[:-1])
                    self.modules_string.append(ms)

    def parse_arguments(self):
        parser = ArgParse(argument_space_count=20, usage="suyambu [options]")
        parser.add_argument(["-help", "-h"], description="show help", is_flag=True)
        parser.add_argument(["-payload", "-p"], example="payload", description="specify the payload you want to generate")
        parser.add_argument(["-host"], example="ip:port", description="specify the listening host and port")
        return parser

    def route(self):
        if self.args.help:
            self.parser.print_help()
            return
        
        try:
            self.cmdloop()
        except KeyboardInterrupt:
            self.postloop()

    def do_use(self, line):
        """load a module to use"""
        try:
            mod = __import__("modules." + line.strip().replace("/", "."), fromlist=["SuyambuModule"]).SuyambuModule()
            can_load = mod.setup()
            if can_load:
                self.module["instance"] = mod
                self.module["name"] = line.strip()
                self.module["commands"].clear()
                for cmd in dir(mod):
                    if cmd.startswith("do_"):
                        self.module["commands"].append(cmd)
                    elif cmd.startswith("complete_"):
                        setattr(self, cmd, getattr(mod, cmd))
                self.update_prompt()
            else:
                log.error("Unable to load '{}' setup failed".format(line))
        except (ModuleNotFoundError, ValueError):
            log.error("Module not found: {}".format(line))
        except AttributeError:
            log.error("It is not a Suyambu module")

    def update_prompt(self):
        if self.module["name"] is not None:
            nodes = self.module["name"].split("/")
            if len(nodes) == 1:
                self.prompt = "{} {}({}) > ".format(underline(green("suyambu")), red(nodes[0]), yellow(nodes[-1]))
            else:
                head_node = nodes.pop(0)
                self.prompt = "{} {}({}) > ".format(underline(green("suyambu")), red(head_node), yellow("_".join(nodes)))
        else:
            self.prompt = "{} > ".format(underline(green("suyambu")))

    def completenames(self, text, *ignored):
        dotext = "do_"+text
        return [a[3:] for a in self.get_names() + self.module["commands"] if a.startswith(dotext)]

    def complete_use(self, text, line, begidx, endidx):
        mline = line.partition(" ")[2]
        offs = len(mline) - len(text)
        return [s[offs:] for s in self.modules_string if s.startswith(mline)]

    def default(self, line):
        nodes = line.split(" ")
        if "do_" + nodes[0].strip() in self.module["commands"] and self.module["instance"] is not None:
            getattr(self.module["instance"], "do_" + nodes[0].strip())(" ".join(nodes[1:]).strip())
        else:
            log.info("Exec: {}\n".format(line))
            os.system(line)

    def do_help(self, line):
        """show available commands use cases"""
        print("\nCore Commands:\n")
        meths = dir(self)
        for meth in meths:
            if meth.startswith("do_"):
                s = meth.replace("do_", "")
                doc = getattr(self, meth).__doc__
                if doc is None:
                    doc = "-"
                print("{}{}: {}".format(s, " " * (10 - len(s)), doc))
        print()

        if self.module["instance"] is not None:
            print("Module Commands:\n")
            for meth in self.module["commands"]:
                s = meth.replace("do_", "")
                doc = getattr(self.module["instance"], meth).__doc__
                if doc is None:
                    doc = "-"
                print("{}{}: {}".format(s, " " * (10 - len(s)), doc))
            print()


if __name__ == "__main__":
    suyambu = Suyambu()
    suyambu.route()
