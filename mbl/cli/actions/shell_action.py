#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Shell action handler."""


from mbl.cli.utils import ssh

from . import utils


def execute(args):
    """Entry point for the shell action."""
    dev = utils.create_device(args.address, args.config_hostname)

    with ssh.SSHSession(dev) as ssh_session:
        if args.cmd:
            if not args.quiet:
                print("Running a command on the device...")
            ssh_session.run_cmd(args.cmd, check=True, writeout=not args.quiet)
        else:
            if not args.quiet:
                print("Starting an interactive shell...")
            ssh_session.start_shell()
