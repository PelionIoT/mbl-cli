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
)


class ArgumentParserWithDefaultHelp(argparse.ArgumentParser):
    """Subclass that always shows the help message on invalid arguments."""

    def error(self, message):
        """Error handler."""
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        raise SystemExit(2)


def parse_args(description):
    """Parse the command line args."""
    parser = ArgumentParserWithDefaultHelp(
        description=description,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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

    get = command_group.add_parser("get", help="Get a file from the device.")
    get.add_argument(
        "--address",
        help="The ipv4 or ipv6 address of the device"
        " you want to communicate with. ",
    )
    get.add_argument(
        "src_path", help="Path of the file you're getting on the device."
    )
    get.add_argument(
        "dst_path",
        help="Destination path on the host"
        " where the file will be transferred to.",
    )
    get.set_defaults(func=get_action.execute)

    put = command_group.add_parser("put", help="Put a file on the device.")
    put.add_argument(
        "-a",
        "--address",
        help="The ipv4 or ipv6 address"
        " of the device you want to communicate with. ",
    )
    put.add_argument(
        "src_path", help="Local path to the file you want to transfer."
    )
    put.add_argument(
        "dst_path",
        help="Destination path on the device where the file"
        " will be transferred to.",
    )
    put.set_defaults(func=put_action.execute)

    shell = command_group.add_parser(
        "shell",
        help="Run a single command or "
        "enable an interactive shell. "
        "If -c flag, followed by the command, is passed then the "
        "command will run, "
        "if no command is passed an interactive shell is started",
    )
    shell.add_argument(
        "-c",
        "--cmd",
        help="Run a command on the device. "
        "If the command contains spaces, "
        "enclose in single quotes. Example: 'ls -la'",
        default=str(),
    )
    shell.add_argument(
        "--address",
        help="The ipv4 or ipv6 address of"
        " the device you want to communicate with. ",
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
