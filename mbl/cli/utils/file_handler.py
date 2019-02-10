#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Handle data files."""

import json
import os
import pathlib
import shutil
import tempfile

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


def to_binary_file(file_path, binary_data):
    _write_with_copy_modify_move(file_path, binary_data)


def from_json(config_file_path):
    """Read data from a json file.

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


def to_json(config_file_path, **store_conf_data):
    """Write a dictionary of config data to a json file.

    :param config_file_path Path: Path object representing the file-to-write.
    """
    json_fmt_data = json.dumps(store_conf_data)
    _write_with_copy_modify_move(config_file_path, json_fmt_data)


def _write_with_copy_modify_move(file_path, data):
    """Write data to a file safely.

    Check the file exists and create it if not.
    Use copy-modify-move when writing to avoid corrupting the config_file.

    :param file_path Path: Path object representing the file-to-write.
    """
    file_path.touch(exist_ok=True)
    # copy the config file to a tmp file
    tmp_dir = tempfile.mkdtemp(dir=str(file_path.parent))
    try:
        # copy2 will attempt to preserve all metadata
        dst_path = shutil.copy2(str(file_path), tmp_dir)
        # write the data to the tmp file
        with open(dst_path, "w") as dfile:
            dfile.write(data)
        # move the tmp file over the original file
        shutil.move(dst_path, str(file_path))
    finally:
        shutil.rmtree(tmp_dir)


# This is going to be removed.
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
