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
    provision_action,
    save_api_key_action,
    pelion_status_action,
)


def parse_args(description):
    """Parse the command line args."""
    parser = ArgumentParserWithDefaultHelp(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-V",
        "--version",
        help="Show the version and exit.",
        action="store_true",
    )
    parser.add_argument(
        "-a",
        "--address",
        help="The ipv4/6 address or hostname of the device"
        " you want to communicate with. ",
    )
    parser.add_argument(
        "-v", "--verbose", help="Enable verbose logging.", action="store_true"
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

    save_api_key.add_argument("key", help="The API key to store.")
    save_api_key.set_defaults(func=save_api_key_action.execute)

    provision = command_group.add_parser("provision-pelion")
    provision.add_argument(
        "dev_cert_name",
        help="Name of the developer certificate to fetch (or create and store "
        "if -c is also given). "
        "Certificates can only be fetched if they've already been added "
        "to the Team Store.",
    )
    provision.add_argument(
        "update_cert_name",
        help="Name of the update certificate to fetch (or parse from an "
        "update_default_resources.c file and store if -p is given). "
        "Certificates can only be fetched if they've already been added "
        "to the Team Store.",
    )
    provision.add_argument(
        "-p",
        "--parse-update-cert",
        help="Parse an existing update certificate and save it in the"
        " Team Store.",
        metavar="CERT_PATH",
        dest="update_cert_path",
    )
    provision.add_argument(
        "-c",
        "--create-dev-cert",
        action="store_true",
        help="Create a new developer certificate.",
    )
    provision.set_defaults(func=provision_action.execute)

    query_pelion = command_group.add_parser("get-pelion-status")
    query_pelion.set_defaults(func=pelion_status_action.execute)

    args_namespace = parser.parse_args()

    # We want to fail gracefully, with a consistent
    # help message, in the no argument case.
    # So here's an obligatory hasattr hack.
    if not hasattr(args_namespace, "func") and not args_namespace.version:
        parser.error("No arguments given!")
    else:
        return args_namespace


class ArgumentParserWithDefaultHelp(argparse.ArgumentParser):
    """Subclass that always shows the help message on invalid arguments."""

    def error(self, message):
        """Error handler."""
        sys.stderr.write("error: {}\n".format(message))
        self.print_help()
        raise SystemExit(2)


def _load_description_text():
    help_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "help.txt"
    )
    with open(help_path) as hfile:
        return hfile.read()
