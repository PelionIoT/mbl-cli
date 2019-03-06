#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Creates an enumerated list of strings."""

from collections import UserList


class IndexedTextList(UserList):
    """List of strings. Numbered according to index."""

    def __str__(self):
        """Return all list items as multi-line string."""
        self.sort(key=lambda x: x.split(": ")[1])
        output_string = str()
        for index, item in enumerate(self):
            output_string += "{}: {}\n".format(index+1, item)
        return output_string
