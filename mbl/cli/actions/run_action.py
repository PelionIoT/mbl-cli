#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Entry point for the run action."""


from mbl.cli.utils import ssh

from . import utils


def execute(args):
    """Run action handler."""
    dev = utils.create_device(args)
    print(f"Running the command {args.cmd} on device: {dev.hostname}\n")

    with ssh.SSHSession(dev) as ssh_session:
        ssh_session.run(args.src_path, args.dst_path)

    print("\nCompleted without error.")
