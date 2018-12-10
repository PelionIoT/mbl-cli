#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""List action handler."""


import argparse
import sys

from mbl.cli.utils import discovery, print_list

from . import utils


def execute(args):
    """Entry point for the list action."""
    print(
        "Discovering devices. "
        f"This will take up to {discovery.TIMEOUT} seconds."
    )
    dev_notifier = discovery.DeviceDiscoveryNotifier()
    lister = print_list.TextList(list())
    dev_notifier.add_listener(lister.add)

    discovery.do_discovery(dev_notifier)

    if not lister.data:
        raise IOError("No devices found!")
    else:
        enumerated_things = lister.show()
        print("\n".join(enumerated_things))
        return enumerated_things
