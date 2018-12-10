#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Shell action handler."""


import sys

from mbl.cli.utils import shell, ssh

from . import utils


def execute(args):
    """Entry point for the shell action."""
    dev = utils.create_device(args)

    with ssh.SSHSession(dev) as ssh_session:
        if args.cmd:
            print(f"Running a command on the device...")
            ssh_session.run(args.cmd)
        else:
            print(f"Starting an interactive shell...")
            ssh_session.start_shell()
