#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""The Mbed Linux OS CLI.

A toolbox for managing target devices running Mbed Linux OS.
"""

import sys

from mbl.cli.args import parser


def _main():
    try:
        args = parser.parse_args(__doc__)
        args.func(args)
    except Exception as error:
        print(error)
        return 1
    else:
        return 0
