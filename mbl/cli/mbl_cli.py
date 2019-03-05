#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""The Mbed Linux OS CLI.

A toolbox for managing target devices running Mbed Linux OS.
"""

import enum
import sys
import traceback

from mbl.cli.args import parser


class ExitCode(enum.Enum):
    """Application return codes."""
    SUCCESS = 0
    ERROR = 256


def _main():
    try:
        args = parser.parse_args(description=__doc__)
        args.func(args)
    except Exception as error:
        if hasattr(error, "return_code"):
            ret_code = error.return_code
        else:
            ret_code = ExitCode.ERROR.value
        if args.verbose:
            traceback.print_exc()
        else:
            print(error, file=sys.stderr)
        return ret_code
    else:
        return 0
