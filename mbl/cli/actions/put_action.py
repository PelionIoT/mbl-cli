#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Put action handler."""


from mbl.cli.utils import ssh

from . import utils


def execute(args):
    """Entry point for the put action."""
    dev = utils.create_device(args.address)
    print("Putting {} on device: {}\n".format(args.src_path, dev.hostname))

    with ssh.SSHSession(dev) as ssh_session:
        ssh_session.put(
            local_path=args.src_path,
            remote_path=args.dst_path,
            recursive=args.recursive,
        )

    print("\n\nTransfer completed.")
