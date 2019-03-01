#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Action handler helper functions/classes."""

import functools
import socket

from mbl.cli.utils import device, file_handler, ssh


# The path to the "pelion-provisioning-util" utility on the target.
# Lives here until there's a need to move it to its own file.
PROVISIONING_UTIL_PATH = "/opt/arm/pelion-provisioning-util"


def ssh_session(func):
    """
    SSH session decorator. 
    This decorator will handle SSH connection and teardown.
    Decorate a function with this and give it an 'ssh' kwarg.
    The decorator passes in an instance of SSHSession to the ssh kwarg. 
    """
    # retain metadata from the 'wrapped' function 'object'.
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with ssh.SSHSession(
            device.create_device(**file_handler.read_device_file())
        ) as session:
            func(*args, **kwargs, ssh=session)

    return wrapper


def create_device(args):
    """Create a device from either a file or args, depending on args.

    :param args Namespace: args from the cli parser.
    """
    if args.address:
        if is_valid_ipv4_address(args.address) or is_valid_ipv6_address(
            args.address
        ):
            data = {"hostname": "", "address": args.address}
        else:
            raise ValueError("Invalid address given.")
    else:
        data = file_handler.read_device_file()
    return device.create_device(**data)


def is_valid_ipv4_address(address):
    """Validate an ipv4 address."""
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count(".") == 3
    except socket.error:
        return False
    else:
        return True


def is_valid_ipv6_address(address):
    """Validate an ipv6 address."""
    address, *_ = address.split("%")
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    else:
        return True
