#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""List certificate argument handler."""

from mbl.cli.utils import cloudapi, store


def execute(args):
    """Entry point for the 'list-dev-cert' command."""
    key = store.Store("user").api_key
    api = cloudapi.DevCredentialsAPI(key)
    print(
        "Developer certificates in Pelion Device Management: "
        "\n{}".format("\n".join(api.existing_cert_names)),
        end="\n\n",
    )
    print(
        "Developer and update certificates in local storage:\n"
        "{}".format(
            "\n".join(list(store.Store("team").certificate_paths.keys()))
        ),
        end="\n\n",
    )
