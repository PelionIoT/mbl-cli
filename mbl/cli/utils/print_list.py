#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Creates an enumerated list of strings."""

import sys


class TextList:
    """Shows a list of things and allows you to add items."""

    def __init__(self, data):
        """:param data list: collection of data to display/choose from."""
        self.data = list(data)

    def add(self, item):
        """Add an item to the list."""
        self.data.append(item)

    def show(self):
        """Return an enumerated list of things."""
        enumerated_things = list()
        for index, item in enumerate(self.data):
            enumerated_things.append("{}: {}".format(index + 1, item))
        return enumerated_things
