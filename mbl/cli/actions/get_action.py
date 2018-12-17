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
    print(f"Getting {args.src_path} from device: {dev.hostname}\n")

    with ssh.SSHSession(dev) as ssh_session:
        with utils.ProgressSpinnerContext() as spinner:
            ssh_session.get(args.src_path, args.dst_path)

    print("\nCompleted without error.")