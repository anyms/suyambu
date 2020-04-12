#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""

import re
import sys

from utils import log
from utils.formatter import format_space


class Args:
    def __init__(self):
        pass


class ArgParse:
    def __init__(self, argument_space_count, usage):
        self.log = log
        self.argument_space_count = argument_space_count
        self.usage = usage
        self.commandline_arguments = []
        for arg in sys.argv[1:]:
            if arg.find("=") > -1:
                for a in arg.split("="):
                    self.commandline_arguments.append(a)
            else:
                self.commandline_arguments.append(arg)

        self.args = Args()
        self.arguments = []
    
    def print_help(self):
        s = "usage: {}\n\n".format(self.usage)
        for argument in self.arguments:
            other_flags = ""
            for flag in argument["other_flags"]:
                other_flags += ", {}".format(flag)
            if argument["example"] is not None:
                s += "{} : {}\n".format(format_space(argument["flag"] + other_flags + " " + argument["example"], self.argument_space_count), argument["description"])
            else:
                s += "{} : {}\n".format(format_space(argument["flag"] + other_flags, self.argument_space_count), argument["description"])
        s += """
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""
        print(s)
        
    def set_attr(self, flag, value):
        is_set = False
        for arg in self.arguments:
            if flag in arg["other_flags"]:
                setattr(self.args, arg["flag"], value)
                is_set = True
                break
            
        if not is_set:
            setattr(self.args, flag, value)
        

    def parse(self):
        # setting up args
        for argument in self.arguments:
            flag = argument["flag"].replace("-", "")
            if argument["is_flag"]:
                self.set_attr(flag, False)
            else:
                self.set_attr(flag, None)

        # update args
        for argument in self.arguments:
            flag = argument["flag"].replace("-", "")
            for i, cmd_argument in enumerate(self.commandline_arguments):
                if (argument["flag"] == cmd_argument or cmd_argument in argument["other_flags"]) and argument["is_flag"]:
                    self.set_attr(flag, True)
                elif argument["flag"] == cmd_argument or cmd_argument in argument["other_flags"]:
                    try:
                        if argument["pattern"] is not None:
                            if re.compile(argument["pattern"]).match(self.commandline_arguments[i + 1]):
                                self.set_attr(flag, self.commandline_arguments[i + 1])
                            else:
                                print("[Error] flag {} does not match the pattern.".format(argument["flag"]))
                                sys.exit(1)
                        else:
                            self.set_attr(flag, self.commandline_arguments[i + 1])
                    except IndexError:
                        pass

        for argument in self.arguments:
            if argument["is_required"]:
                flag = argument["flag"].replace("-", "")
                if getattr(self.args, flag) is None or getattr(self.args, flag) == False:
                    self.log.error("flag {} is required".format(argument["flag"]))
                    sys.exit(1)
        return self.args

    def add_argument(self, flag, example=None, description=None, is_flag=False, pattern=None, is_required=False):
        if type(flag) is str:
            self.arguments.append({
                "flag": flag,
                "example": example,
                "description": description,
                "is_flag": is_flag,
                "pattern": pattern,
                "is_required": is_required,
                "other_flags": []
            })
        else:
            self.arguments.append({
                    "flag": flag[0],
                    "example": example,
                    "description": description,
                    "is_flag": is_flag,
                    "pattern": pattern,
                    "is_required": is_required,
                    "other_flags": flag[1:]
                })