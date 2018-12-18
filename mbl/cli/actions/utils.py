#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Action handler helper functions/classes."""

import pathlib
import re
import sys
import threading
import time

from mbl.cli.utils import device, file_handler, ssh


JSON_FILE_PATH = str(pathlib.Path().home() / ".mbl-dev.json")


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


def create_device(args):
    """Create a device from either a file or args, depending on args.

    :param args Namespace: args from the cli parser.
    """
    if args.address:
        return device.create_device("", args.address)
    else:
        return _create_device_from_data(_read_device_file())


def save_device_info(device, path=JSON_FILE_PATH):
    """Save device info to a file."""
    fh = file_handler.DeviceInfoFileHandler(path)
    fh.save_device_data(device)


def is_ipv6_addr(address):
    """Match an ipv6 address string."""
    return False


def is_ipv4_addr(address):
    """Match an ipv4 address string."""
    ipv4_matcher = r"(\d{1,3}?\.){3}(\d{1,3})"
    return re.compile(ipv4_matcher).fullmatch(address)


class ProgressSpinnerContext:
    """The graphical majesty of an ascii progress spinner in its own thread."""

    def __init__(self):
        """Init the spinning joy."""
        self.spin_stop_event = threading.Event()

    def __enter__(self):
        """Enter the spinner thread context."""
        spin_thread = threading.Thread(
            target=show_progress_spinner, args=(self.spin_stop_event,)
        )
        spin_thread.start()
        return self

    def __exit__(self, *exception_info):
        """Exit and shut down the spinny thread."""
        self.spin_stop_event.set()
        return exception_info


def show_progress_spinner(event):
    """'Draw' a spinning cursor."""
    for spinner in spinning_cursor():
        sys.stdout.write(spinner)
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write("\b")
        if event.is_set():
            return


def spinning_cursor():
    """Iterate through the characters required for a spinning cursor effect."""
    while True:
        for cursor in "|/-\\":
            yield cursor
