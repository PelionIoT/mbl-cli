#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Parser for the cli."""

import argparse
import sys

from mbl.cli.actions import (
    get_action,
    list_action,
    put_action,
    select_action,
    shell_action,
    which_action,
)


class ArgumentParserWithDefaultHelp(argparse.ArgumentParser):
    """Subclass that always shows the help message on invalid arguments."""

    def error(self, message):
        """Error handler."""
        sys.stderr.write("error: {}\n".format(message))
        self.print_help()
        raise SystemExit(2)


def parse_args(description):
    """Parse the command line args."""
    parser = ArgumentParserWithDefaultHelp(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-a",
        "--address",
        help="The ipv4 or ipv6 address of the device"
        " you want to communicate with. ",
    )

    command_group = parser.add_subparsers(
        description="The commands you can run on the device."
    )

    lister = command_group.add_parser(
        "list", help="List all devices on the network."
    )
    lister.set_defaults(func=list_action.execute)

    select = command_group.add_parser(
        "select",
        help="Select a device from a list of all devices on the network.",
    )
    select.set_defaults(func=select_action.execute)

    which = command_group.add_parser(
        "which", help="Show the currently selected device."
    )
    which.set_defaults(func=which_action.execute)

    get = command_group.add_parser("get", help="Get a file from the device.")
    get.add_argument(
        "src_path", help="Path of the file you're getting on the device."
    )
    get.add_argument(
        "dst_path",
        help="Destination path on the host"
        " where the file will be transferred to.",
    )
    get.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Get the contents of a directory recursively.",
    )
    get.set_defaults(func=get_action.execute)

    put = command_group.add_parser("put", help="Put a file on the device.")
    put.add_argument(
        "src_path", help="Local path to the file you want to transfer."
    )
    put.add_argument(
        "dst_path",
        help="Destination path on the device where the file"
        " will be transferred to.",
    )
    put.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Put the contents of a directory recursively.",
    )
    put.set_defaults(func=put_action.execute)

    shell = command_group.add_parser(
        "shell",
        help="Run a single command or "
        "enable an interactive shell. "
        "If followed by a command, the "
        "command will run, and the output is printed to stdout. "
        "If no command is passed an interactive shell is started.",
    )
    shell.add_argument(
        "cmd",
        nargs="?",
        help="Run a command on the device. "
        "If the command contains spaces, "
        "enclose in single quotes. Example: 'ls -la'",
    )
    shell.set_defaults(func=shell_action.execute)

    args_namespace = parser.parse_args()

    # We want to fail gracefully, with a consistent
    # help message, in the no argument case.
    # So here's an obligatory hasattr hack.
    if not hasattr(args_namespace, "func"):
        parser.error("No arguments given!")
    else:
        return args_namespace
