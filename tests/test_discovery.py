#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import socket
from collections import namedtuple
from unittest import mock

import pytest

from mbl.cli.utils import discovery as d


@pytest.fixture
def discovery():
    with mock.patch("mbl.cli.utils.discovery.zeroconf") as zconf:
        device_listener = d.DeviceDiscoveryNotifier()
        yield device_listener, zconf
        d.DeviceDiscoveryNotifier.devices = list()


class TestDeviceDiscovery:
    @pytest.mark.parametrize(
        "properties, address, service_type, name",
        [
            (
                {b"mblos": False},
                socket.inet_aton("168.224.0.4"),
                "_ssh._tcp.local.",
                "mbed-linux-os-8379._ssh._tcp.local.",
            ),
            (
                {b"mblos": True},
                socket.inet_aton("254.255.255.255"),
                "_ssh._tcp.local.",
                "mbed-linux-os-0._ssh._tcp.local.",
            ),
            (
                {b"mblos": False},
                socket.inet_aton("192.254.255.0"),
                "_ssh._tcp.local.",
                "johnsdev._ssh._tcp.local.",
            ),
            (
                {b"mblos": True},
                socket.inet_aton("254.255.255.255"),
                "_ssh._tcp.local.",
                "my_iot.nonsense._ssh._tcp.local.",
            ),
        ],
    )
    def test_single_valid_device_discovered(
        self, discovery, properties, address, service_type, name
    ):
        def callbk(item):
            assert item.split(":")[0] == name.split("." + service_type)[0]

        device_listener, zconf = discovery
        data = namedtuple("ServiceInfo", "properties address")
        data.properties = properties
        data.address = address
        zconf.get_service_info.return_value = data
        device_listener.add_listener(callbk)
        device_listener.add_service(zconf, service_type, name)

        zconf.get_service_info.assert_called_once_with(service_type, name)
        assert device_listener.devices

    @pytest.mark.parametrize(
        "properties, address, service_type, name",
        [
            (
                ({b"mblos": False}, {b"mblos": False}),
                (
                    socket.inet_aton("168.224.0.4"),
                    socket.inet_aton("168.224.76.4"),
                ),
                "_ssh._tcp.local.",
                (
                    "mbed-linux-os-8379._ssh._tcp.local.",
                    "mbed-linux-os-8820._ssh._tcp.local.",
                ),
            ),
            (
                ({b"mblos": False}, {b"mblos": True}),
                (
                    socket.inet_aton("168.224.245.0"),
                    socket.inet_aton("168.2.66.1"),
                ),
                "_ssh._tcp.local.",
                (
                    "mbed-linux-os-2315._ssh._tcp.local.",
                    "jim._ssh._tcp.local.",
                ),
            ),
        ],
    )
    def test_multiple_valid_devices_discovered(
        self, discovery, properties, address, service_type, name
    ):
        data1 = namedtuple("ServiceInfo", "properties address")
        data2 = namedtuple("ServiceInfo", "properties address")

        device_listener, zconf = discovery
        data1.properties = properties[0]
        data1.address = address[0]
        data2.properties = properties[1]
        data2.address = address[1]
        zconf.get_service_info.return_value = data1
        device_listener.add_service(zconf, service_type, name[0])

        zconf.get_service_info.return_value = data2
        device_listener.add_service(zconf, service_type, name[1])

        assert len(device_listener.devices) == 2
        assert (
            device_listener.devices[0].hostname
            != device_listener.devices[1].hostname
        )

    @pytest.mark.parametrize(
        "properties, address, service_type, name",
        [
            (
                {b"mblos": False},
                "1683.4224.0.4.",
                "_ssh._tcp.local.",
                "mbed-linux-os-8379._ssh._tcp.local.",
            ),
            (
                {b"mblos": True},
                "254.255.255.255.004",
                "_ssh._tcp.local.",
                "mbed-linux-os-0._ssh._tcp.local.",
            ),
            (
                {b"mblos": False},
                "192.254.255.___£",
                "_ssh._tcp.local.",
                "johnsdev._ssh._tcp.local.",
            ),
            (
                {b"mblos": True},
                "254.255.ham.255",
                "_ssh._tcp.local.",
                "my_iot.nonsense._ssh._tcp.local.",
            ),
        ],
    )
    def test_device_discovery_invalid_ips(
        self, discovery, properties, address, service_type, name
    ):
        device_listener, zconf = discovery
        data = namedtuple("ServiceInfo", "properties address")

        with pytest.raises(OSError):
            data.properties = properties
            data.address = socket.inet_aton(address)
            zconf.get_service_info.return_value = data
            device_listener.add_service(zconf, service_type, name)

        assert len(device_listener.devices) == 0

    @pytest.mark.parametrize(
        "properties, address, service_type, name",
        [
            (
                {b"sobl": False},
                socket.inet_aton("168.224.0.4"),
                "_ssh._tcp.local.",
                "mbed-linux-os-8379._ssh._tcp.local.",
            ),
            (
                {b"slobm": True},
                socket.inet_aton("254.255.255.255"),
                "_ssh._tcp.local.",
                "mbed-linux-os-0._ssh._tcp.local.",
            ),
            (
                {b"ham": False},
                socket.inet_aton("192.254.255.0"),
                "_ssh._tcp.local.",
                "johnsdev._ssh._tcp.local.",
            ),
            (
                {b"009109": True},
                socket.inet_aton("254.255.255.255"),
                "_ssh._tcp.local.",
                "my_iot.nonsense._ssh._tcp.local.",
            ),
        ],
    )
    def test_device_discovery_non_mblos_devices(
        self, discovery, properties, address, service_type, name
    ):
        device_listener, zconf = discovery
        data = namedtuple("ServiceInfo", "properties address")

        data.properties = properties
        data.address = address
        zconf.get_service_info.return_value = data
        device_listener.add_service(zconf, service_type, name)

        assert len(device_listener.devices) == 0
