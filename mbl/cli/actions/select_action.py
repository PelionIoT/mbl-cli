#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Select action handler."""


import sys

from mbl.cli.utils import device, file_handler

from . import list_action


def execute(args):
    """Entry point for the select command."""
    list_of_devices = list_action.execute(args)
    user_input = input("\nSelect a device from the list: \n")
    try:
        user_input = int(user_input)
        selected_device = list_of_devices[user_input - 1]
        index, name, addr = selected_device.split(": ")
    except (ValueError, IndexError):
        raise IndexError("Enter a valid device index as shown in the list.")
    else:
        dev = device.create_device(name, addr)
        file_handler.save_device_info(dev)
