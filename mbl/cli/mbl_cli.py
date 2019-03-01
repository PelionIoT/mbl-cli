#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""The Mbed Linux OS CLI.

A toolbox for managing target devices running Mbed Linux OS.
"""

import sys
import traceback

from mbl.cli.args import parser


def _main():
    try:
        args = parser.parse_args(description=__doc__)
        args.func(args)
    except Exception as error:
        if args.verbose:
            traceback.print_exc()
        else:
            print(error, file=sys.stderr)
        return 1
    else:
        return 0
