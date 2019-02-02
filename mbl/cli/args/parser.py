#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Parser for the cli."""

import argparse
import sys
import os

from mbl.cli.actions import (
    get_action,
    list_action,
    put_action,
    select_action,
    shell_action,
    which_action,
    save_api_key_action,
)


def parse_args(description):
    """Parse the command line args."""
    parser = ArgumentParserWithDefaultHelp(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-a",
        "--address",
        help="The ipv4/6 address or hostname of the device"
        " you want to communicate with. ",
    )

    command_group = parser.add_subparsers(
        title="mbl-cli supports the following commands",
        description=_load_description_text(),
    )

    lister = command_group.add_parser("list")
    lister.set_defaults(func=list_action.execute)

    select = command_group.add_parser("select")
    select.set_defaults(func=select_action.execute)

    which = command_group.add_parser("which")
    which.set_defaults(func=which_action.execute)

    get = command_group.add_parser("get")
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

    put = command_group.add_parser("put")
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

    shell = command_group.add_parser("shell")
    shell.add_argument(
        "cmd",
        nargs="?",
        help="Run a command on the device. "
        "If the command contains spaces, "
        "enclose in single quotes. Example: 'ls -la'",
    )
    shell.set_defaults(func=shell_action.execute)

    save_api_key = command_group.add_parser("save-api-key")
    save_api_key.add_argument(
        "uid", help="UID/name of the persistent storage location."
    )
    save_api_key.add_argument(
        "--new-store",
        nargs=2,
        metavar=("PATH", "CONTEXT"),
        help="""Create a new store. PATH and CONTEXT are required.
        PATH: file path for the new store.
        CONTEXT: storage context (must be either 'team' or 'user').""",
    )
    save_api_key.add_argument(
        "keys", nargs="+", help="The API key(s) to store."
    )
    save_api_key.set_defaults(func=save_api_key_action.execute)

    args_namespace = parser.parse_args()

    # Extra logic here to check the `save-api-key --new-store` option
    # was given the correct values.
    if hasattr(args_namespace, "new_store"):
        _validate_new_store_arg(args_namespace.new_store)
    # We want to fail gracefully, with a consistent
    # help message, in the no argument case.
    # So here's an obligatory hasattr hack.
    if not hasattr(args_namespace, "func"):
        parser.error("No arguments given!")
    else:
        return args_namespace


class ArgumentParserWithDefaultHelp(argparse.ArgumentParser):
    """Subclass that always shows the help message on invalid arguments."""

    def error(self, message):
        """Error handler."""
        sys.stderr.write(f"error: {message}\n")
        self.print_help()
        raise SystemExit(2)


def _load_description_text():
    help_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "help.txt"
    )
    with open(help_path) as hfile:
        return hfile.read()


def _validate_new_store_arg(arg):
    _, context = arg
    if context not in ["team", "user"]:
        raise ValueError("--new-store CONTEXT must be 'team' or 'user'")
