#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Entry point for the pelion-provision command."""

import os

from mbl.cli.utils.cloudapi import (
    DevCredentialsAPI,
    parse_existing_update_cert,
)
from mbl.cli.utils.store import Store


def execute(args):
    """Handle the provision-pelion command."""
    cert_name = args.dev_cert_name
    if args.create_dev_cert:
        cert_data = _create_certificate(
            _get_api_key(), cert_name
        )
        _save_certificate(cert_name, cert_data)
    else:
        cert_data = _get_certificate_paths(cert_name)
    update_resource = parse_existing_update_cert(args.update_cert_path)
    _save_certificate(
        os.path.basename(args.update_cert_path), update_resource
    )


def _get_api_key():
    store_handle = Store("user")
    try:
        return list(store_handle.api_keys.values())[0]
    except IndexError:
        raise RuntimeError("You have not added and API key to the store.")


def _get_certificate_paths(cert_name):
    sh = Store("team")
    return sh.certificate_paths[cert_name]


def _create_certificate(api_key, cert_name):
    credentials_api = DevCredentialsAPI(api_key)
    return credentials_api.create_dev_credentials(cert_name)


def _save_certificate(cert_name, cert_data):
    team_store_handle = Store("team")
    team_store_handle.add_certificate(cert_name, cert_data)
