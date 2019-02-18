#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Tests for SCP transfer validation."""

import pytest
from unittest import mock

from mbl.cli.utils import ssh
import os
import io
import shutil


@pytest.fixture(
    params=[
        ("mydir", "tools.txt"),
        ("tools.txt", "mydir"),
        ("", "tools.txt"),
        ("tools.txt", ""),
    ]
)
def file_paths(tmp_path, request):
    """Mock file paths and fake transfer files for 'validation'."""
    local_ = tmp_path / request.param[0]
    mock_remote = tmp_path / request.param[1]
    try:
        if ".txt" not in request.param[0]:
            local_.mkdir(exist_ok=True)
        else:
            local_.touch(exist_ok=True)
            try:
                shutil.copy(str(local_), str(mock_remote))
            except shutil.SameFileError:
                pass
        if ".txt" not in request.param[1]:
            mock_remote.mkdir(exist_ok=True)
        else:
            mock_remote.touch(exist_ok=True)
            try:
                shutil.copy(str(mock_remote), str(local_))
            except shutil.SameFileError:
                pass
    except FileExistsError:
        pass
    yield local_, mock_remote


@pytest.fixture
def mock_ssh_cmd():
    """Mock the SSSession.run_cmd method and hashlib."""
    # This closure is used to monkeypatch run_cmd.
    def run_cmd_side_effect(input_val):
        """Mock run_cmd return values based on input_val."""
        if os.path.isdir(input_val.split(" ")[1]):
            return (
                io.BytesIO(b""),
                io.BytesIO(b""),
                io.BytesIO(b"Is a directory"),
            )
        else:
            return (
                io.BytesIO(b""),
                io.BytesIO(b"HASH filename"),
                io.BytesIO(b""),
            )

    with mock.patch("mbl.cli.utils.ssh.hashlib") as hsh_lib:
        with mock.patch.object(
            ssh.SSHSession, "run_cmd", side_effect=run_cmd_side_effect
        ) as run_cmd_mock:
            yield run_cmd_mock, hsh_lib


class Device:
    """Fake device to instantiate SSHSession with."""

    hostname = ""


class TestSCPFileTransferValidation:
    """Test the single file validation function."""

    def test_file_validation_succeeds_on_all_valid_inputs(
        self, file_paths, mock_ssh_cmd
    ):
        """Check the function gets to the hash comparison and it passes."""
        hsh_lib = mock_ssh_cmd[1]
        hsh_lib.md5().hexdigest.return_value = "HASH"
        session = ssh.SSHSession(Device())
        try:
            session._validate_file_transfer(
                str(file_paths[0]), str(file_paths[1])
            )
        except ssh.SCPValidationFailed as io_error:
            pytest.fail("Raised SCPValidationFailed {}".format(io_error))

    def test_file_validation_raises_with_unique_hashes(
        self, file_paths, mock_ssh_cmd
    ):
        """Test SCPValidationFailed is raised when hashes are unequal."""
        hsh_lib = mock_ssh_cmd[1]
        hsh_lib.md5().hexdigest.return_value = "HASHY"
        session = ssh.SSHSession(Device())
        with pytest.raises(ssh.SCPValidationFailed):
            session._validate_file_transfer(
                str(file_paths[0]), str(file_paths[1])
            )
