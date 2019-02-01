#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Entry point for save-api-key action."""

from mbl.cli.utils import store, file_handler


def execute(args):
    """Execute the save-api-key action."""
    store_handle = store.Store(
        uid=args.uid,
        location=args.location,
        store_type=args.context,
        api_keys=args.key,
    )
    store_handle.add_api_keys(args.key)
    store_handle.save()
