#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Delete certificate argument handler."""

from mbl.cli.utils import cloudapi
from mbl.cli.utils.store import Store


def execute(args):
    """Handle delete certificate actions."""
    key = Store("user").api_key
    api = cloudapi.DevCredentialsAPI(key)
    if args.name in api.existing_cert_names:
        print("Deleting certificate from Device Management.")
        api.delete_developer_certificate(args.name)
    print("Deleting certificate locally.")
    Store("team").delete_certificate(args.name)
    print("Certificate '{}' was deleted.".format(args.name))
