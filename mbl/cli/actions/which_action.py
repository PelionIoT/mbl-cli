#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Which action handler."""


import sys

from mbl.cli.utils import device, file_handler

from . import utils


def execute(args):
    """Entry point for which action."""
    args.address = None
    device = utils.create_device(args)
    print("{} ({})".format(device.hostname, device.address))
