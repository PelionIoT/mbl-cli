#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Shell action handler."""


from mbl.cli.utils import ssh

from . import utils


def execute(args):
    """Entry point for the shell action."""
    dev = utils.create_device(args.address)

    with ssh.SSHSession(dev) as ssh_session:
        if args.cmd:
            print("Running a command on the device...")
            stdin, stdout, stderr = ssh_session.run_cmd(args.cmd)
            for line in stdout.read().splitlines():
                print(line.decode())
        else:
            print("Starting an interactive shell...")
            ssh_session.start_shell()
