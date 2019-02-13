#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Test command handler functions."""

from unittest import mock

import pytest

from mbl.cli.actions import get_action, list_action, put_action, select_action
from mbl.cli.utils import device


@pytest.fixture
def discovery():
    """Mock avahi discovery."""
    with mock.patch("mbl.cli.utils.discovery._avahi_browse") as avahi:
        avahi.return_value = (
            b"=;eth3;ipv6;mbed-linux-os-9999;mdns;local;"
            b"mbed-linux-os-9999.local;fe80::d079:8191:9140:c56;22;mblos"
        )
        yield avahi


@pytest.fixture
def save_dev_info_mock():
    """Mock save_device_info."""
    with mock.patch("mbl.cli.utils.file_handler.save_device_info") as sdi_mock:
        yield sdi_mock


@pytest.fixture
def mock_ssh():
    """Mock ssh handler."""
    with mock.patch(
        "mbl.cli.utils.ssh.SSHSession", autospec=True
    ) as ssh_session:
        with mock.patch(
            "mbl.cli.utils.ssh.scp.SCPClient", autospec=True
        ) as scp_mock:
            scp_mock.return_value.__enter__.return_value = scp_mock
            ssh_session.return_value.__enter__.return_value = ssh_session
            yield ssh_session, scp_mock


class Args:
    """Mock args namespace."""

    address = ""
    src_path = ""
    dst_path = ""
    recursive = False


class TestListCommand:
    """List cmd tests."""

    def test_list_command_produces_text_list(self, discovery):
        """Check a text list is produced and formatted correctly."""
        text_list = list_action.execute(Args())
        assert text_list == [
            r"1: mbed-linux-os-9999: fe80::d079:8191:9140:c56%eth3"
        ]


class TestSelectCommand:
    """Select cmd tests."""

    @pytest.fixture
    def mock_input(self):
        """Mock the input() builtin."""
        input_mock = mock.MagicMock(spec=input)
        with mock.patch.object(
            select_action, "input", input_mock, create=True
        ) as _mock_input:
            yield _mock_input

    @pytest.fixture
    def mock_list(self):
        """Mock the list command function."""
        list_mock = mock.MagicMock()
        with mock.patch.object(
            select_action, "list_action", list_mock, create=True
        ) as _mock_list:
            yield _mock_list

    def test_select_saves_device(
        self, save_dev_info_mock, mock_input, mock_list
    ):
        """Test save_device_info called with correct args."""
        mock_list.execute.return_value = [
            r"1: mbed-linux-os-9999: fe80::d079:8191:9140:c56%eth3"
        ]
        mock_input.return_value = "1"
        select_action.execute(Args())
        save_dev_info_mock.assert_called_once_with(
            device.create_device(
                r"mbed-linux-os-9999", r"fe80::d079:8191:9140:c56%eth3"
            )
        )

    @pytest.mark.parametrize("input_val", ["0", "a", "-1", "2"])
    def test_select_raises_on_invalid_input(
        self, save_dev_info_mock, mock_input, mock_list, input_val
    ):
        """Test appropriate errors are raised on invalid device selections."""
        with pytest.raises(IndexError):
            mock_list.execute.return_value = [
                r"1: mbed-linux-os-9999: fe80::d079:8191:9140:c56%eth3"
            ]
            mock_input.return_value = input_val
            select_action.execute(Args())


class TestGetCommand:
    """Test the get command."""

    @pytest.fixture(
        params=[
            ("some/path/file.txt", "remote/path/", "168.254.56.92"),
            (
                "some/path/file.txt",
                "remote/path/file.txt",
                "fe80::6593:97d5:5bb6:d182%26",
            ),
        ]
    )
    def args(self, request):
        """Parametrized args fixture."""
        _args = Args()
        _args.src_path = request.param[0]
        _args.dst_path = request.param[1]
        _args.address = request.param[2]
        yield _args

    def test_get(self, mock_ssh, args):
        """Test the get command is executed without error."""
        _ssh, _scp = mock_ssh
        get_action.execute(args)
        assert _ssh.return_value.__enter__.called
        _ssh.get.assert_called_once_with(
            args.src_path, args.dst_path, args.recursive
        )
        assert _ssh.return_value.__exit__.called


class TestPutCommand:
    """Test the put command."""

    @pytest.fixture(
        params=[
            ("some/path/file.txt", "remote/path/", "168.254.56.92"),
            (
                "some/path/",
                "remote/path/file.txt",
                "fe80::6593:97d5:5bb6:d182%26",
            ),
        ]
    )
    def args(self, request):
        """Parametrized args fixture."""
        _args = Args()
        _args.src_path = request.param[0]
        _args.dst_path = request.param[1]
        _args.address = request.param[2]
        yield _args

    def test_put(self, mock_ssh, args):
        """Test the put command is executed without error."""
        _ssh, _scp = mock_ssh
        put_action.execute(args)
        assert _ssh.return_value.__enter__.called
        _ssh.put.assert_called_once_with(
            args.src_path, args.dst_path, args.recursive
        )
        assert _ssh.return_value.__exit__.called
