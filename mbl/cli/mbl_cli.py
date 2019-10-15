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
import pkg_resources
from mbl.cli.args import parser


class ExitCode(enum.Enum):
    """Application return codes."""

    SUCCESS = 0
    ERROR = 255


def _print_version():
    print(pkg_resources.get_distribution("mbl-cli").version)
    return ExitCode.SUCCESS.value


def _run(args):
    args.func(args)


def _set_error_code(error):
    if hasattr(error, "return_code"):
        return error.return_code
    else:
        return ExitCode.ERROR.value


def _print_error_message(msg, verbose=False):
    if verbose:
        traceback.print_exc()
    else:
        print(msg, file=sys.stderr)


def _main():
    try:
        args = parser.parse_args(description=__doc__)

        if args.version:
            return _print_version()

        # Run a command
        _run(args)

    except Exception as error:
        _print_error_message(error, args.verbose)
        return _set_error_code(error)

    except KeyboardInterrupt:
        _print_error_message("User quit.", args.verbose)
        return ExitCode.ERROR.value

    return ExitCode.SUCCESS.value
