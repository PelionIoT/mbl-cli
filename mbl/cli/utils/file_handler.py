#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Handle data files."""

import json
import os
import pathlib

DEVICE_FILE_PATH = str(pathlib.Path().home() / ".mbl-dev.json")
STORE_LOCATION_FILE_PATH = pathlib.Path().home() / ".mbl-stores.json"


def read_device_file(path=DEVICE_FILE_PATH):
    """Read the json file and return some data."""
    fh = JSONParser(path)
    try:
        device_data = fh.from_file()
    except FileNotFoundError:
        raise IOError("Please select a device or provide an ip address.")
    else:
        return device_data


def save_device_info(device, path=DEVICE_FILE_PATH):
    """Save device info to a file."""
    fh = JSONParser(path)
    fh.to_file(device._asdict())


def read_known_stores():
    """Read the store locations file."""
    STORE_LOCATION_FILE_PATH.touch(exist_ok=True)
    fh = JSONParser(STORE_LOCATION_FILE_PATH.resolve())
    try:
        return fh.from_file()
    except json.JSONDecodeError:
        return dict()


def write_store_config(
    config_file_path=STORE_LOCATION_FILE_PATH, mode="w+", **store_conf_data
):
    """Write to a store config file."""
    config_file_path.touch(exist_ok=True)
    fh = JSONParser(config_file_path.resolve())
    fh.to_file(store_conf_data, mode=mode)


class JSONParser:
    """Read and write JSON data to files."""

    JSON_EXT = ".json"

    def __init__(self, dfile_path):
        """:param dfile_path str: path to the json file."""
        if not os.path.splitext(dfile_path)[1] == self.JSON_EXT:
            raise TypeError("Data file path must be a path to a json file.")
        self.data_file_path = str(dfile_path)

    def from_file(self):
        """Read the data from the filecache, return a json object."""
        with open(self.data_file_path, "r") as dfile:
            return json.load(dfile)

    def to_file(self, data, mode="w+"):
        """Write data to a file in JSON format.

        :param dict data: key/value pairs to dump to a JSON file.
        """
        json_fmt_data = json.dumps(data)
        with open(self.data_file_path, mode) as dfile:
            dfile.write(json_fmt_data)
