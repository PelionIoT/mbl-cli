#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""File io tests."""

from io import StringIO
from unittest import mock

import pytest

from mbl.cli.utils import device, file_handler


@pytest.fixture
def fh():
    """Instance of DeviceFileHandler."""
    yield file_handler.JSONParser("test.json")


@pytest.fixture
def mock_open():
    """Mock the builtin open function."""
    open_mock = mock.MagicMock(spec=open)
    read_mock = mock.MagicMock(spec=StringIO)
    open_mock.return_value.__enter__.return_value = read_mock

    with mock.patch.object(file_handler, "open", open_mock, create=True):
        yield open_mock, read_mock


@pytest.fixture
def mock_json(mock_open):
    """Mock the json library."""
    json_mock = mock.MagicMock()
    with mock.patch.object(file_handler, "json", json_mock, create=True):
        yield json_mock


class TestFileHandler:
    """File handler tests."""

    def test_save_device_data(self, fh, mock_open):
        """Test open is called with correct arguments."""
        open_mock, read_mock = mock_open
        dev = device.DeviceInfo(
            "mbed-linux-nbakjal", "169.254.0.8", "root", ""
        )
        fh.to_file(dev._asdict())
        assert open_mock.call_args[0] == (fh.data_file_path, "w+")

    def test_load_device_data(self, fh, mock_json):
        """Test json.load is called."""
        fh.from_file()
        assert mock_json.load.called
