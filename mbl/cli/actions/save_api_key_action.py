#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Entry point for save-api-key action."""

from mbl.cli.utils.store import Store
from mbl.cli.utils.cloudapi import find_api_key_name


def execute(args):
    """Execute the save-api-key action."""
    store_handle = Store("user")
    name = find_api_key_name(args.key)
    store_handle.add_api_key(name, args.key)
    store_handle.save()
