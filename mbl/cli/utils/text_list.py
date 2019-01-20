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
        return "\n".join(self)

    def append(self, item):
        """Append item as a string with numbered index."""
        super().append(f"{len(self)+1}: {item}")
