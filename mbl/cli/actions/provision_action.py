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
from mbl.cli.utils.device import create_device
from mbl.cli.utils.file_handler import read_device_file
from mbl.cli.utils.ssh import SSHSession
from mbl.cli.utils.store import Store

from . import utils


def execute(args):
    """Handle the provision-pelion command."""
    dev_cert_name = args.dev_cert_name
    update_cert_name = args.update_cert_name
    if args.update_cert_path:
        # parse and save the update certificate data in the team store
        update_cert_data = parse_existing_update_cert(args.update_cert_path)
        _save_certificate(update_cert_name, update_cert_data)
    if args.create_dev_cert:
        # Create a dev cert using the Pelion Service API and save it.
        dev_cert_data = _create_certificate(_get_api_key(), dev_cert_name)
        _save_certificate(dev_cert_name, dev_cert_data)
    # get the parsed certificate data file paths from the store
    dev_cert_paths = _get_certificate_paths(dev_cert_name)
    update_cert_paths = _get_certificate_paths(update_cert_name)
    # transfer the certificates to the device and provision it
    # by calling an on-device module.
    target_dir = "/scratch/provisioning-certs"
    _prepare_remote_dir(target_dir)
    try:
        _transfer_certs_to_device(
            dev_cert_paths, update_cert_paths, target_dir
        )
        _provision_device()
    finally:
        _remove_remote_dir(target_dir)


def _get_api_key():
    store_handle = Store("user")
    key = store_handle.api_key
    if not key:
        raise AttributeError("You have not added an API key to the store.")
    return key


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


@utils.ssh_session
def _prepare_remote_dir(target_dir, ssh):
    # rm any existing /provisioning-certs directory on the target.
    # It's fine for this to fail silently as usually we don't
    # expect this directory to exist.
    ssh.run_cmd("rm -r {}".format(target_dir))
    # create a fresh `target_dir`
    ssh.run_cmd("mkdir -p {}".format(target_dir), check=True)


@utils.ssh_session
def _transfer_certs_to_device(
    dev_cert_paths, update_cert_paths, target_dir, ssh
):
    dev_dir = os.path.dirname(dev_cert_paths[0])
    update_dir = os.path.dirname(update_cert_paths[0])
    # transfer the certificate payloads to the device
    ssh.put(dev_dir, target_dir, recursive=True)
    ssh.put(update_dir, target_dir, recursive=True)
    # move all files to the `target_dir` root for pelion-provisioning-util
    dev_folder_path = os.path.join(target_dir, os.path.basename(dev_dir))
    ssh.run_cmd("mv {}/* {}".format(dev_folder_path, target_dir), check=True)
    update_folder_path = os.path.join(target_dir, os.path.basename(update_dir))
    ssh.run_cmd(
        "mv {}/* {}".format(update_folder_path, target_dir), check=True
    )


@utils.ssh_session
def _remove_remote_dir(path, ssh):
    ssh.run_cmd("rm -r {}".format(path), check=False)


@utils.ssh_session
def _provision_device(ssh):
    ssh.run_cmd(
        "/opt/arm/pelion-provisioning-util --provision",
        check=True,
        writeout=True,
    )
