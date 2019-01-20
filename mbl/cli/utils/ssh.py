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
import io
import paramiko
import scp

from . import shell


def scp_progress(filename, size, sent):
    """Display the progress of an scp transfer."""
    if sent:
        try:
            fname = filename.decode()
        except AttributeError:
            fname = filename
        sys.stdout.write(
            "{} is transferring. Progress: {}%\r".format(
                fname, int(sent / size * 100)
            )
        )


def scp_session(transfer_func):
    """Start an scp session on the client.

    Use as a decorator.
    """
    # wrapper
    @functools.wraps(transfer_func)
    def wrapper(self, local_path, remote_path, recursive=False):
        with scp.SCPClient(
            self._client.get_transport(), progress=scp_progress
        ) as scp_client:
            transfer_func(
                self,
                local_path=local_path,
                remote_path=remote_path,
                scp_client=scp_client,
                recursive=recursive,
            )
            self._validate_scp_transfer(
                local_path=local_path,
                remote_path=remote_path,
                recursive=recursive,
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
    def put(self, local_path, remote_path, recursive, scp_client=None):
        """Send data via scp."""
        scp_client.put(
            local_path, remote_path=remote_path, recursive=recursive
        )

    @scp_session
    def get(self, remote_path, local_path, recursive, scp_client=None):
        """Get data via scp."""
        scp_client.get(remote_path, local_path, recursive=recursive)

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

    def _validate_scp_transfer(self, local_path, remote_path, recursive=False):
        """Ensure an SCP transfer succeeded."""
        if recursive:
            self._validate_directory_transfer(local_path, remote_path)
        else:
            self._validate_file_transfer(local_path, remote_path)

    def _validate_file_transfer(self, local_path, remote_path):
        local_basename = os.path.basename(local_path)
        remote_basename = os.path.basename(remote_path)
        remote_stdout = ""
        remote_stderr = ""
        while not remote_stdout:
            remote_cmd_output = self.run_cmd("md5sum {}".format(remote_path))
            remote_stdout = remote_cmd_output[1].read().decode()
            remote_stderr = remote_cmd_output[2].read().decode()
            if "Is a directory" in remote_stderr:
                remote_path = os.path.join(remote_path, local_basename)
                continue
        remote_file_checksum = remote_stdout.split(" ")[0]
        local_file_checksum = ""
        while not local_file_checksum:
            try:
                with open(local_path, "rb") as local_file:
                    local_file_checksum = hashlib.md5(
                        local_file.read()
                    ).hexdigest()
                    break
            except IsADirectoryError:
                local_path = os.path.join(local_path, remote_basename)
                continue
        if local_file_checksum != remote_file_checksum:
            raise SCPValidationFailed(
                "\nRemote file md5sum: {}\nLocal file md5sum: {}\n"
                "\nYour file may not have been transferred correctly!".format(
                    remote_file_checksum, local_file_checksum
                )
            )

    def _validate_directory_transfer(self, local_path, remote_path):
        local_basename = os.path.basename(local_path)
        remote_basename = os.path.basename(remote_path)

        remote_file_checksums = (
            self.run_cmd(
                "for fd in `find {} -type f`; do md5sum $fd;".format(
                    remote_path
                )
            )[0]
            .read()
            .decode()
            .split("\n")[0]
        )
        print(remote_file_checksums)


class SCPValidationFailed(Exception):
    """SCP transfer md5 validation failed."""
