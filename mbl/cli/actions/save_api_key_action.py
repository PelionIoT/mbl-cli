#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Entry point for save-api-key action."""

from mbl.cli.utils import store


def execute(args):
    """Execute the save-api-key action."""
    if args.new_store:
        store_path, context = args.new_store
        store_handle = store.create(args.uid, context, store_path)
    else:
        store_handle = store.get(args.uid)
    store_handle.api_keys.extend(args.keys)
    store_handle.save()
