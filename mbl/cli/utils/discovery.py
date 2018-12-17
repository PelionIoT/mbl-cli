#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Module handles device discovery."""

import platform
import socket
import subprocess
import sys
import time
from collections import namedtuple

import zeroconf

from mbl.cli.utils import device, events

MBL_ID = b"mblos"
TIMEOUT = 30
SLEEP_TIME = 0.5


class DeviceDiscoveryNotifier(events.Notifier):
    """Observer of the zeroconf service.

    Propagates notifications on to listeners when a new device is added.
    """

    devices = list()

    def add_service(self, zeroconf, service_type, name):
        """Called when a new zeroconf service is discovered.

        Ensure it's an 'mbed linux device', notify listeners if it is.
        """
        info = zeroconf.get_service_info(service_type, name)

        try:
            info.properties[MBL_ID]
        except KeyError:
            return
        else:
            try:
                inet_addr = socket.inet_ntoa(info.address)
            except (OSError, TypeError):
                inet_addr = info.address

            new_dev = device.create_device(name, inet_addr)
            if new_dev not in self.devices:
                self.devices.append(new_dev)
                name = name.split(f".{service_type}")
                self.notify(f"{name[0]}: {new_dev.address}")

    def remove_service(self, zeroconf, type, name):
        """Remove services from the list.

        We don't need it (at the moment) but zeroconf wants an override.
        """
        pass


class DeviceGetter:
    """Browse for ssh services on the local network."""

    ADDR = "_ssh._tcp.local."

    def __init__(self):
        """Initialise Zeroconf."""
        self.zconf = zeroconf.Zeroconf()

    def __enter__(self):
        """Enter the context, return self."""
        return self

    def __exit__(self, *exception_info):
        """Exit the context, close zeroconf."""
        self.zconf.close()
        return exception_info

    def discover_all(self, listener):
        """Browse for ssh services on the network."""
        self.browser = zeroconf.ServiceBrowser(self.zconf, self.ADDR, listener)


class ServiceData:
    """Enum of service data entries."""

    interface = 1
    family = 2
    name = 3
    stype = 4
    area = 5
    hostname = 6
    ip = 7
    port = 8
    prop = 9


def parse_avahi_output():
    """Poll avahi, pack output data into a data struct.

    Yield the data structs for each service.
    """
    hostname = "name"
    address = "address"
    properties = "properties"
    raw_output = b""
    end_time = time.time() + TIMEOUT
    known_device_cache = list()

    while not raw_output and (time.time() < end_time):
        raw_output = subprocess.Popen(
            [
                "avahi-browse",
                "--terminate",
                "--resolve",
                "--no-fail",
                "-p",
                "_ssh._tcp",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        ).communicate()[0]
        time.sleep(SLEEP_TIME)

    output = dict()
    for txt_line in raw_output.split(b"\n"):
        if txt_line.startswith(b"="):
            tokens = txt_line.split(b";")
            if tokens[ServiceData.name] in known_device_cache:
                continue
            output[hostname] = tokens[ServiceData.name]
            output[address] = "{}%{}".format(
                tokens[ServiceData.ip].decode(),
                tokens[ServiceData.interface].decode(),
            )
            output[properties] = {tokens[ServiceData.prop].strip(b'"'): False}
        if len(output) == 3:
            yield output
            known_device_cache.append(output[hostname])
            output.clear()


class AvahiZeroconf:
    """Pack avahi output text into a struct.

    This basically exists to mock out the zeroconf
    class when using avahi for discovery.
    """

    ServiceInfo = namedtuple("ServiceInfo", "name properties address")

    def __init__(self, **kwargs):
        """:param kwargs dict: data to pass into ServiceInfo."""
        self.service_info = self.ServiceInfo(**kwargs)

    def get_service_info(self, name, addr):
        """Just return the ServiceInfo struct ignoring args (yikes)."""
        return self.service_info


def do_discovery(listener):
    """Browse for mblos devices for up to TIMEOUT seconds."""
    if platform.system() == "Linux":
        for src_info in parse_avahi_output():
            listener.add_service(
                AvahiZeroconf(**src_info), "local", src_info["name"].decode()
            )
    else:
        with DeviceGetter() as dev_getter:
            end_time = time.time() + TIMEOUT
            while not listener.devices and (time.time() < end_time):
                time.sleep(SLEEP_TIME)
                dev_getter.discover_all(listener)
            # one more scan to check for more devices
            if len(listener.devices) is 1:
                time.sleep(SLEEP_TIME)
                dev_getter.discover_all(listener)