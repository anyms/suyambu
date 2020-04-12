#!/usr/bin/env python3
# coding=utf-8

"""
Copyright (c) 2019 suyambu developers (http://suyambu.net/framework)
See the file 'LICENSE' for copying permission
"""


class Table:
    def __init__(self):
        self._rows = {}

    def __repr__(self):
        return self.pretty_print()

    def add(self, header, cols):
        self._rows[header] = cols

    def pretty_print(self):
        s = ""
        padding = 2
        headers = list(self._rows.keys())
        max_lengths = []
        for header in headers:
            
            # find the max width of the column
            max_length = len(header)
            for col in self._rows[header]:
                if len(col) > max_length:
                    max_length = len(col)

            max_lengths.append(max_length)

        for i, header in enumerate(headers):
            s += "{}{}{}".format(header, " " * (max_lengths[i] - len(header)), " " * padding)
        s += "\n"
        for i, header in enumerate(headers):
            s += "{}{}".format("-" * max_lengths[i], " " * padding)
        s += "\n"

        for i, _ in enumerate(self._rows[headers[0]]):
            for j, header in enumerate(headers):
                s += "{}{}{}".format(self._rows[header][i], " " * (max_lengths[j] - len(self._rows[header][i])), " " * padding)
            s += "\n"
        s+="\n"
        return s