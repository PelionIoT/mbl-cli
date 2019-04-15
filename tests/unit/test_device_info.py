#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Test the DeviceInfo data structure."""


import pytest
from mbl.cli.utils import device


class TestDeviceInfo:
    """Test DeviceInfo's eq/ne operators."""

    def test_compares_eq(self):
        """Test equivalent devices compare equal."""
        dev_a = device.create_device("john", "102.2034.04.05")
        dev_b = device.create_device("john", "102.2034.04.05")

        assert dev_a == dev_b

    @pytest.mark.parametrize(
        "hostname, address",
        [
            (("john", "103.2034.04.05"), ("john", "102.2034.04.05")),
            (("jim", "103.2034.04.05"), ("john", "102.2034.04.05")),
        ],
    )
    def test_compares_ne(self, hostname, address):
        """Test differing devices compare not equal."""
        dev_a = device.create_device(hostname[0], address[0])
        dev_b = device.create_device(hostname[1], address[1])
        assert dev_a != dev_b

    @pytest.mark.parametrize(
        "dev_a, dev_b",
        [
            (
                device.create_device("john", "103.2034.04.05"),
                ("john", "102.2034.04.05"),
            ),
            (
                device.create_device("jim", "103.2034.04.05"),
                ["john", "102.2034.04.05"],
            ),
        ],
    )
    def test_eq_raises_on_invalid_types(self, dev_a, dev_b):
        """Test raises a TypeError when trying to compare invalid types."""
        with pytest.raises(TypeError):
            dev_a == dev_b

    @pytest.mark.parametrize(
        "dev_a, dev_b",
        [
            (
                device.create_device("john", "103.2034.04.05"),
                ("john", "102.2034.04.05"),
            ),
            (
                device.create_device("jim", "103.2034.04.05"),
                ["john", "102.2034.04.05"],
            ),
        ],
    )
    def test_ne_raises_on_invalid_types(self, dev_a, dev_b):
        """Test raises a TypeError when trying to compare invalid types."""
        with pytest.raises(TypeError):
            dev_a != dev_b
