#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""pelion-status action handler."""

from mbl.cli.utils.ssh import SSHSession
from mbl.cli.actions import utils


def execute(args):
    """Entry point for the get-pelion-status command."""
    device = utils.create_device(args)
    with SSHSession(device) as ssh:
        ssh.run_cmd(
            "/opt/arm/pelion-provisioning-util --get-pelion-status",
            check=True,
            writeout=True,
        )
