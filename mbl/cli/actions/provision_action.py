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
from mbl.cli.utils.device import create_device
from mbl.cli.utils.file_handler import read_device_file
from mbl.cli.utils.ssh import SSHSession


def execute(args):
    """Handle the provision-pelion command."""
    dev_cert_name = args.dev_cert_name
    update_cert_name = os.path.basename(args.update_cert_path)
    # parse and save the update certificate to a directory in the team store
    update_cert_data = parse_existing_update_cert(args.update_cert_path)
    _save_certificate(update_cert_name, update_cert_data)
    if args.create_dev_cert:
        dev_cert_data = _create_certificate(_get_api_key(), dev_cert_name)
        _save_certificate(dev_cert_name, dev_cert_data)
    # get the parsed certificate data file paths from the store
    dev_cert_paths = _get_certificate_paths(dev_cert_name)
    update_cert_paths = _get_certificate_paths(update_cert_name)
    # transfer the certificates to the device and provision it
    # by calling an on-device module.
    _transfer_certs_to_device(dev_cert_paths, update_cert_paths)
    _provision_device()


def _get_api_key():
    store_handle = Store("user")
    try:
        return list(store_handle.api_keys.values())[0]
    except IndexError:
        raise RuntimeError("You have not added an API key to the store.")


def _get_certificate_paths(cert_name):
    sh = Store("team")
    try:
        return sh.certificate_paths[cert_name]
    except KeyError:
        raise ValueError(
            "Certificate '{}' not found in the store.".format(cert_name)
        )


def _create_certificate(api_key, cert_name):
    credentials_api = DevCredentialsAPI(api_key)
    return credentials_api.create_dev_credentials(cert_name)


def _save_certificate(cert_name, cert_data):
    team_store_handle = Store("team")
    team_store_handle.add_certificate(cert_name, cert_data)


def _transfer_certs_to_device(dev_cert_paths, update_cert_paths):
    target_dir = "/scratch/provisioning-certs"
    device = create_device(**read_device_file())
    dev_dir = os.path.basename(dev_cert_paths[0])
    update_dir = os.path.dirname(update_cert_paths[0])
    with SSHSession(device) as ssh_session:
        ssh_session.put(dev_dir, target_dir, recursive=True)
        ssh_session.put(update_dir, target_dir, recursive=True)


def _provision_device():
    device = create_device(**read_device_file())
    with SSHSession(device) as ssh_session:
        ssh_session.run_cmd("/opt/arm/provision-pelion --kcm-item-store")
