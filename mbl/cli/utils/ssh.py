#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
 
"""Handle ssh connections and data transfer."""


import functools
import paramiko
import platform

from . import shell


def sftp_session(func):
    """Decorator to start an sftp session on the client."""
    # wrapper
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        with self._client.open_sftp() as sftp:
            return func(self, *args, sftp, **kwargs)

    return wrapper


class SSHClientNoAuth(paramiko.SSHClient):
    """SSH Client which handles 'no auth' SSH devices."""

    def _auth(self, username, *args):
        """Override to invoke the transport directly when SSH auth is None."""
        self._transport.auth_none(username)
        return


class SSHSession:
    """Context manager wrapping an SSHClient, handles setup/auth and sftp."""

    def __init__(self, device):
        """:param device DeviceInfo: A device info object."""
        self.device = device
        self._client = SSHClientNoAuth()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        """Enter the context, connect to the ssh session."""
        self._client.connect(
            self.device.address,
            username=self.device.username,
            password=self.device.password,
        )
        return self

    def __exit__(self, *exception_info):
        """Exit the context, ensuring the ssh session is closed."""
        self._client.close()
        return exception_info

    @sftp_session
    def put(self, local_path, remote_path, sftp=None):
        """Send data via sftp."""
        sftp.put(local_path, remote_path)

    @sftp_session
    def get(self, remote_path, local_path, sftp=None):
        """Get data via sftp."""
        sftp.get(remote_path, local_path)

    def start_shell(self):
        """Start an interactive shell."""
        if platform.system() == "Windows":
            return shell.WindowsSSHShell(self._client.invoke_shell())
        else:
            return shell.PosixSSHShell(self._client.invoke_shell())

    def run_cmd(self, cmd):
        """Execute a command."""
        try:
            cmd_output = self._client.exec_command(cmd)
        except paramiko.SSHException as ssh_error:
            raise IOError(
                "The command `{}` failed to execute, "
                "the error was: {}".format(cmd, ssh_error)
            )
        else:
            return cmd_output
