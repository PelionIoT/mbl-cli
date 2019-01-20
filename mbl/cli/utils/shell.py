#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""SSH shell module."""

import functools
import select
import socket
import struct
import sys

from abc import abstractmethod


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
        while True:
            rlist, wlist, elist = select.select([self.chan, sys.stdin], [], [])
            # check how many bytes are waiting to be read
            buffered_raw = fcntl_.ioctl(
                rlist[0].fileno(), termios_.FIONREAD, "  "
            )
            buffer_size = struct.unpack("h", buffered_raw)[0]
            # read ssh input and write to stdout
            if self.chan in rlist:
                try:
                    try:
                        chan_input = self.chan.recv(1024).decode()
                    except UnicodeDecodeError:
                        continue
                    if not chan_input:
                        sys.stdout.write("\r\nShell terminated.\r\n")
                        break
                    else:
                        sys.stdout.write(chan_input)
                        sys.stdout.flush()
                except socket.timeout:
                    pass
            # send stdin to the ssh channel
            if sys.stdin in rlist:
                # read all waiting bytes from stdin
                stdin = sys.stdin.read(buffer_size)
                if not stdin:
                    break
                else:
                    self.chan.send(stdin)


class WindowsSSHShell(SSHShell):
    """Windows terminal IO."""

    def run(self):
        """Terminal IO."""
        import threading

        def write_to_stdout(channel):
            while True:
                data = channel.recv(1024).decode()
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
        ).start()
        try:
            while True:
                stdin_data = sys.stdin.read(1)
                if not stdin_data:
                    write_task.join()
                    raise EOFError
                else:
                    self.chan.send(stdin_data)
        except EOFError:
            pass
