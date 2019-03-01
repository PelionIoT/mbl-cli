#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""pelion-status action handler."""

import shlex

from mbl.cli.actions import utils
from mbl.cli.utils.ssh import SSHSession

from . import utils


def execute(args):
    """Entry point for the get-pelion-status command."""
    device = utils.create_device(args)
    with SSHSession(device) as ssh:
        ssh.run_cmd(
            "{} --get-pelion-status".format(
                shlex.quote(utils.PROVISIONING_UTIL_PATH)
            ),
            check=True,
            writeout=True,
        )
