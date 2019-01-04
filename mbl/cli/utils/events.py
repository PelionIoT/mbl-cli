#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Low level event handlers."""


class Notifier:
    """Holds a list of listeners, notifies them when told.

    Intended to be subclassed by anyone
    that wants to give event driven notifications.
    """

    def __init__(self):
        """Initialise a list of callbacks."""
        self.callbacks = []

    def add_listener(self, new_listener):
        """Register interest with the notifier.

        :param new_listener function: a callback to notify.
        """
        self.callbacks.append(new_listener)

    def notify(self, *args, **kwargs):
        """Call all listeners."""
        for callback in self.callbacks:
            callback(*args, **kwargs)


class AsyncNotifier(Notifier):
    """Async version of the notifier."""

    async def notify(self, *args, **kwargs):
        """Call all listeners asynchronously."""
        for callback in self.callbacks:
            await callback(*args, **kwargs)
