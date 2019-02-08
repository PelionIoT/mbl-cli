#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Get action handler."""

import sys
import threading
import time

from mbl.cli.utils import ssh

from . import utils


def execute(args):
    """Entry point for the get cli command."""
    dev = utils.create_device(args)
    print("Getting {} from device: {}\n".format(args.src_path, dev.hostname))

    with ssh.SSHSession(dev) as ssh_session:
        ssh_session.get(
            remote_path=args.src_path,
            local_path=args.dst_path,
            recursive=args.recursive,
        )

    print("\n\nCompleted without error.")
