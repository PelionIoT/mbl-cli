#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""SSH shell module."""

import functools
import select
import struct
import shutil
import subprocess
import sys

from abc import abstractmethod

from paramiko.ssh_exception import SSHException

# Maximum number of bytes to read from the ssh channel.
MAX_READ_BYTES = 1024


class ShellTerminate(Exception):
    """SSH data transfer has stopped."""


def termios_tty(func):
    """Create a tty using termios.

    Use as a decorator.
    """
    # termios/tty imports are only available on mac & Linux
    try:
        import termios
        import tty
        import fcntl
    except ImportError:
        return

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
            self.chan.settimeout(0.0)
            func(self, termios, fcntl, **kwargs)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

    return wrapper


class SSHShell:
    """SSH Shell base class. Runs the shell when instantiated."""

    def __init__(self, channel):
        """:param channel Channel: ssh channel that connects to the shell."""
        self.chan = channel
        self.run()

    @abstractmethod
    def run(self):
        """Override to implement platform specific terminal IO."""
        pass


class PosixSSHShell(SSHShell):
    """Posix SSH Shell variant.

    For macOS & Linux.
    """

    @termios_tty
    def run(self, termios_, fcntl_):
        """Terminal IO."""
        while not self.chan.closed:
            rlist, wlist, elist = select.select([self.chan, sys.stdin], [], [])
            buffer_size = self._get_chan_buffer_size(fcntl_, termios_, rlist)
            self._set_tty_size()
            try:
                if self.chan in rlist:
                    self._write_chan_to_stdout()
                if sys.stdin in rlist:
                    self._write_stdin_to_chan(buffer_size)
            except ShellTerminate:
                print("\r\nShell terminated.", end="\r\n")
                break

    def _write_chan_to_stdout(self):
        try:
            chan_input = self.chan.recv(MAX_READ_BYTES).decode()
        except UnicodeDecodeError:
            return
        if not chan_input:
            raise ShellTerminate()
        sys.stdout.write(chan_input)
        sys.stdout.flush()

    def _set_tty_size(self):
        term_size = shutil.get_terminal_size()
        try:
            self.chan.resize_pty(
                width=term_size.columns, height=term_size.lines
            )
        except SSHException:
            return

    def _write_stdin_to_chan(self, buffer_size):
        stdin = sys.stdin.read(buffer_size)
        if not stdin:
            raise ShellTerminate()
        num_bytes = self.chan.send(stdin)
        if not num_bytes:
            raise ShellTerminate()

    def _get_chan_buffer_size(self, fcntl_, termios_, rlist):
        buffered_raw = fcntl_.ioctl(rlist[0].fileno(), termios_.FIONREAD, "  ")
        return struct.unpack("h", buffered_raw)[0]


class WindowsSSHShell(SSHShell):
    """Windows terminal IO."""

    def run(self):
        """Terminal IO."""
        import threading

        def write_to_stdout(channel):
            while True:
                data = channel.recv(MAX_READ_BYTES).decode()
                if not data:
                    sys.stdout.write(
                        "\r\nShell terminated. Press Enter to quit.\r\n"
                    )
                    break
                else:
                    sys.stdout.write(data)
                    sys.stdout.flush()

        write_task = threading.Thread(
            target=write_to_stdout, args=(self.chan,)
        )
        write_task.start()
        try:
            while True:
                stdin_data = sys.stdin.read(1)
                if not stdin_data:
                    write_task.join()
                    raise EOFError()
                else:
                    self.chan.send(stdin_data)
        except EOFError:
            pass
