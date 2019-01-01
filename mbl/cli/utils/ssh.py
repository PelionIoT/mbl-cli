#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Handle ssh connections and data transfer."""


import functools
import hashlib
import os
import platform
import socket
import sys

import paramiko
import scp

from . import shell


def scp_progress(filename, size, sent):
    """Display the progress of an scp transfer."""
    if sent:
        sys.stdout.write(
            "{} is transferring. Progress: {}\r".format(
                filename.decode(), int(sent / size * 100)
            )
        )


def scp_session(func):
    """Decorator to start an scp session on the client."""
    # wrapper
    @functools.wraps(func)
    def wrapper(self, local_path, remote_path):
        with scp.SCPClient(
            self._client.get_transport(), progress=scp_progress
        ) as scp_client:
            func(
                self,
                local_path=local_path,
                remote_path=remote_path,
                scp_client=scp_client,
            )
            self._validate_file_transfer(
                local_path=local_path, remote_path=remote_path
            )

    return wrapper


class SSHClientNoAuth(paramiko.SSHClient):
    """SSH Client which handles 'no auth' SSH devices."""

    def _auth(self, username, *args):
        """Override to invoke the transport directly when SSH auth is None."""
        self._transport.auth_none(username)
        return


class SSHSession:
    """Context manager wrapping an SSHClient, handles setup/auth and scp."""

    def __init__(self, device):
        """:param device DeviceInfo: A device info object."""
        self.device = device
        self._client = SSHClientNoAuth()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        """Enter the context, connect to the ssh session."""
        if self.device.hostname:
            qualified_hostname = f"{self.device.hostname}.local"
        else:
            qualified_hostname = self.device.address
        try:
            self._client.connect(
                qualified_hostname,
                username=self.device.username,
                password=self.device.password,
            )
        except socket.gaierror:
            self._client.connect(
                self.device.address,
                username=self.device.username,
                password=self.device.password,
            )
        return self

    def __exit__(self, *exception_info):
        """Exit the context, ensuring the ssh client is closed."""
        self._client.close()
        return False

    @scp_session
    def put(self, local_path, remote_path, scp_client=None):
        """Send data via scp."""
        scp_client.put(local_path, remote_path=remote_path)

    @scp_session
    def get(self, remote_path, local_path, scp_client=None):
        """Get data via scp."""
        scp_client.get(remote_path, local_path)

    def start_shell(self):
        """Start an interactive shell."""
        if platform.system() == "Windows":
            return shell.WindowsSSHShell(self._client.invoke_shell())
        else:
            return shell.PosixSSHShell(self._client.invoke_shell())

    def run_cmd(self, cmd):
        """Execute a command."""
        try:
            cmd_output = self._client.exec_command(cmd, timeout=30)
        except paramiko.SSHException as ssh_error:
            raise IOError(
                "The command `{}` failed to execute, "
                "the error was: {}".format(cmd, ssh_error)
            )
        else:
            return cmd_output

    def _validate_file_transfer(self, local_path, remote_path):
        """Ensure an SCP file transfer succeeded."""
        local_file_name = os.path.basename(local_path)
        if os.path.basename(remote_path) != local_file_name:
            remote_path = "/".join((remote_path, local_file_name))
        remote_file_checksum = (
            self.run_cmd("md5sum {}".format(remote_path))[1]
            .read()
            .decode()
            .split(" ")[0]
        )
        with open(local_path, "rb") as local_file:
            local_file_checksum = hashlib.md5(local_file.read()).hexdigest()
        if local_file_checksum != remote_file_checksum:
            raise IOError(
                "\nRemote file md5sum: {}\nLocal file md5sum: {}\n"
                "\nYour file may not have been transferred correctly!".format(
                    remote_file_checksum, local_file_checksum
                )
            )
