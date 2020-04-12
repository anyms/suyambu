#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""


class Options:
    def __init__(self):
        self._options = {}

    def __repr__(self):
        return str(self._options)

    def add(self, key, value, description=""):
        self._options[key.upper()] = {
            "value": value,
            "description": description
        }
    
    def get(self, key):
        return self._options[key.upper()]["value"]

    def set(self, key, value):
        if key.upper() in self._options:
            self._options[key.upper()]["value"] = value

    def to_dict(self):
        return self._options
