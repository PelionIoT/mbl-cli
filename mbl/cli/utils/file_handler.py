#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Handle device data files."""

import json
import os


class DeviceInfoFileHandler:
    """Serialise/deserialise DeviceInfo objects to/from json."""

    HOSTNAME_KEY = "hostname"
    ADDRESS_KEY = "addr"
    JSON_EXT = ".json"

    def __init__(self, dfile_path):
        """:param dfile_path str: path to the json file."""
        if not os.path.splitext(dfile_path)[1] == self.JSON_EXT:
            raise TypeError("Data file path must be a path to a json file.")
        self.data_file_path = dfile_path

    def save_device_data(self, device, mode="w+"):
        """Save the device info as a json object.

        :param device DeviceInfo: the DeviceInfo object to serialise.
        :param mode str: optional file mode specifier.
        """
        dev_data = {
            self.HOSTNAME_KEY: device.hostname,
            self.ADDRESS_KEY: device.address,
        }
        json_fmt_data = json.dumps(dev_data)
        with open(self.data_file_path, mode) as dfile:
            dfile.write(json_fmt_data)

    def read_device_data(self):
        """Read the device data from the filecache, return a json object."""
        with open(self.data_file_path, "r") as dfile:
            return json.load(dfile)
