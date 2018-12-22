#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Action handler helper functions/classes."""

import pathlib
import re
import socket
import sys
import threading
import time

from mbl.cli.utils import device, file_handler, ssh

JSON_FILE_PATH = str(pathlib.Path().home() / ".mbl-dev.json")


def create_device(args):
    """Create a device from either a file or args, depending on args.

    :param args Namespace: args from the cli parser.
    """
    if args.address:
        if is_valid_ipv4_address(args.address) or is_valid_ipv6_address(
            args.address
        ):
            return device.create_device("", args.address)
        else:
            return device.create_device(args.address, "")
    else:
        return _create_device_from_data(_read_device_file())


def save_device_info(device, path=JSON_FILE_PATH):
    """Save device info to a file."""
    fh = file_handler.DeviceInfoFileHandler(path)
    fh.save_device_data(device)


def is_valid_ipv4_address(address):
    """Validate an ipv4 address."""
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count(".") == 3
    except socket.error:
        return False
    else:
        return True


def is_valid_ipv6_address(address):
    """Validate an ipv6 address."""
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    else:
        return True


def _read_device_file(path=JSON_FILE_PATH):
    """Read the json file and return some data."""
    fh = file_handler.DeviceInfoFileHandler(path)
    try:
        device_data = fh.read_device_data()
    except FileNotFoundError as file_err:
        raise IOError("Please select a device or provide an ip address.")
    else:
        return device_data


def _create_device_from_data(data):
    """Create a DeviceInfo object using the file data.

    :param data: data as returned from _read_device_file.
    """
    return device.create_device(*data.values())
