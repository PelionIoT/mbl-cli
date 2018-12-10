#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Select action handler."""


import sys

from mbl.cli.utils import device

from . import list_action, utils


def execute(args):
    """Entry point for the select command."""
    list_of_devices = list_action.execute(args)
    user_input = input("\nSelect a device from the list: \n")
    try:
        user_input = int(user_input)
        if user_input <= 0:
            raise IndexError()
        selected_device = list_of_devices[user_input - 1]
        index, name, addr = selected_device.split(": ")
        dev = device.create_device(name, addr)
    except ValueError as err:
        print("Enter a valid device index as shown in the list.")
    except IndexError as index_err:
        print(f"Enter a number between 1 - {len(list_of_devices)}")
    else:
        utils.save_device_info(dev)
