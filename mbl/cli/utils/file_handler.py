#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Handle data files."""

import json
import os
import pathlib

DEVICE_FILE_PATH = str(pathlib.Path().home() / ".mbl-dev.json")


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


def read_config_from_json(config_file_path):
    """Read json data from a file.

    Check the file exists and create it if not.
    We want to return an empty dict and not fail if the file contains no data.

    :param config_file_path Path: Path representing the file-to-read.
    :returns dict: config data (or an empty dict if there was no data).
    """
    config_file_path.touch(exist_ok=True)
    try:
        with open(config_file_path, "r") as dfile:
            return json.load(dfile)
    except json.JSONDecodeError:
        # The file contains no parsable json.
        # In this case return an empty dict.
        return dict()


def write_config_to_json(
    config_file_path="", mode="w+", **store_conf_data
):
    """Write a dictionary of config data to a json file.

    Check the file exists and create it if not.

    :param config_file_path Path: Path object representing the file-to-write.
    :param mode str: file mode (must be one of: 'w', 'w+', 'a', 'a+').
    """
    config_file_path.touch(exist_ok=True)
    json_fmt_data = json.dumps(store_conf_data)
    with open(config_file_path, mode) as dfile:
        dfile.write(json_fmt_data)


class JSONParser:
    """Read and write JSON data to and from a file."""

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
