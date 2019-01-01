#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Classes and functions related to the device abstraction."""

from collections import namedtuple


def create_device(hostname, address, username="root", password=""):
    """Factory function to create a DeviceInfo struct."""
    return DeviceInfo(hostname, address, username, password)


class DeviceInfo(namedtuple("Device", "hostname address username password")):
    """Data structure which holds information pertinent to the device."""

    def __eq__(self, other):
        """== operator."""
        if other.__class__ is self.__class__:
            return (self.hostname == other.hostname) and (
                self.address == other.address
            )
        else:
            raise TypeError(
                "Both objects must be of type"
                f" {self.__class__} or they can't be compared."
            )

    def __ne__(self, other):
        """!= operator."""
        if other.__class__ is self.__class__:
            return not (
                self.hostname == other.hostname
                and self.address == other.address
            )
        else:
            raise TypeError(
                "Both objects must be of type "
                f"{self.__class__} or they can't be compared."
            )
