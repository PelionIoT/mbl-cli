#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Handle ssh connections and data transfer."""


import functools
import hashlib
import os
import platform
import sys
import paramiko
import pathlib
import scp

from . import shell


def scp_progress(filename, size, sent):
    """Display the progress of an scp transfer."""
    if sent:
        try:
            fname = filename.decode()
        except AttributeError:
            fname = filename
        print(
            "\r{} is transferring. Progress {:2.1%}".format(
                fname, sent / size
            ),
            end="\r",
        )
        # vt100 escape sequence to clear current line
        # http://ascii-table.com/ansi-escape-sequences-vt-100.php
        # this will not work on a Windows cmd line, as it doesn't
        # have vt100 support by default.
        # TODO: Windows solution.
        print("\x1b[2K", end="")


def scp_session(transfer_func):
    """Start an scp session on the client.

    SSHSession method decorator.
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

    def run_cmd(self, cmd, check=False, writeout=False):
        """Execute a command over SSH.

        :param cmd str: The shell command to execute over ssh.
        :param check bool: Raise an exception when the cmd returns an error.
        :param writeout bool: Print the returned stdout/err to sys.stdout.
        """
        # closure handles printing stdout/err and optional exception raising
        # on receipt of remote stderr msgs.
        def _check_print_out(ssh_chan_output, check, writeout):
            if check:
                _, stdout, stderr = ssh_chan_output
                if stderr.readable():
                    buf = stderr.read().decode()
                    if buf:
                        msg = "The command returned an error: {}".format(buf)
                        raise SSHCallError(msg)
            if writeout:
                for out_fd in ssh_chan_output:
                    if out_fd.readable():
                        buf = out_fd.read().decode()
                        if buf:
                            print(buf)

        try:
            cmd_output = self._client.exec_command(cmd, timeout=30)
        except paramiko.SSHException as ssh_error:
            raise IOError(
                "The command `{}` failed to execute, "
                "the error was: {}".format(cmd, ssh_error)
            )
        else:
            _check_print_out(cmd_output, check, writeout)
            return cmd_output

    def _validate_scp_transfer(self, local_path, remote_path, recursive=False):
        """Ensure an SCP transfer succeeded."""
        if recursive:
            self._validate_directory_transfer(local_path, remote_path)
        else:
            self._validate_file_transfer(local_path, remote_path)

    def _validate_file_transfer(self, local_path, remote_path):
        rlocal_path, rremote_path = self._resolve_local_and_remote_file_paths(
            local_path, remote_path
        )
        _, out, err = self.run_cmd("md5sum {}".format(rremote_path))
        remote_file_checksum = out.read().decode().split(" ")[0]
        with open(rlocal_path, "rb") as local_file:
            local_file_checksum = hashlib.md5(local_file.read()).hexdigest()
        if local_file_checksum != remote_file_checksum:
            raise SCPValidationFailed(
                "\nRemote file md5sum: {}\nLocal file md5sum: {}\n"
                "\nYour file may not have been transferred correctly!".format(
                    remote_file_checksum, local_file_checksum
                )
            )

    def _validate_directory_transfer(self, local_path, remote_path):
        rlocal_path, rrem_path = self._resolve_local_and_remote_dir_paths(
            local_path, remote_path
        )
        local_hashes, remote_hashes = str(), str()
        local_subpaths = pathlib.Path(rlocal_path).glob("**/*")
        for path in local_subpaths:
            if path.is_file():
                rem_abspath = os.path.join(rrem_path, path.name)
                _, out, err = self.run_cmd(
                    """ md5sum "{}" """.format(rem_abspath)
                )
                remote_hashes += out.read().decode().split()[0]
                with open(str(path), "rb") as file_to_hash:
                    local_hashes += hashlib.md5(
                        file_to_hash.read()
                    ).hexdigest()
        if local_hashes != remote_hashes.strip():
            raise SCPValidationFailed(
                "\nRemote files md5sum: {}\nLocal files md5sum: {}\n"
                "\nYour files may not have been transferred correctly!".format(
                    remote_hashes, local_hashes
                )
            )

    def _resolve_local_and_remote_dir_paths(self, local_path, remote_path):
        local_path = local_path.rstrip(os.sep)
        remote_path = remote_path.rstrip("/")
        local_dirname = os.path.basename(local_path)
        remote_dirname = os.path.basename(remote_path)
        if local_dirname != remote_dirname:
            _, out, err = self.run_cmd("ls -la {}".format(remote_path))
            if local_dirname != "." and local_dirname in out.read().decode():
                # remote_path is the parent directory (or "."),
                # resolve the full path to the target dir just transferred.
                return local_path, os.path.join(remote_path, local_dirname)
            elif remote_dirname != "." and remote_dirname in os.listdir(
                local_path
            ):
                # local_path is the parent directory (or "."),
                # resolve the full path to the target dir just transferred.
                return os.path.join(local_path, remote_dirname), remote_path
            return local_path, remote_path

    def _resolve_local_and_remote_file_paths(self, local_path, remote_path):
        local_path = local_path.rstrip(os.sep)
        remote_path = remote_path.rstrip("/")
        local_basename = os.path.basename(local_path)
        remote_basename = os.path.basename(remote_path)
        if os.path.isdir(local_path):
            local_path = os.path.join(local_path, remote_basename)
        elif os.path.isfile(local_path):
            if local_basename != remote_basename:
                remote_path = os.path.join(remote_path, local_basename)
        else:
            raise IOError(
                "Paths could not be resolved.\nLocal path: {}"
                "\nRemote path: {}".format(local_path, remote_path)
            )
        return local_path, remote_path


class SCPValidationFailed(Exception):
    """SCP transfer md5 validation failed."""


class SSHCallError(Exception):
    """SSH remote command failed."""
