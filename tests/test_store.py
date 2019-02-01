#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Tests for the Store classes."""

import pathlib
from unittest import mock

import pytest

from mbl.cli.utils import store


VALID_INPUTS = [
    {"location": "user", "store_type": "user", "uid": "rob"},
    {"location": "team", "store_type": "team", "uid": "dev-team"},
]

INVALID_INPUTS = [
    {"location": "", "store_type": "user", "uid": "rob"},
    {"location": "", "store_type": "team", "uid": "dev-team"},
    {"location": "", "store_type": "user", "uid": "otheruser"},
    {"location": "", "store_type": "team", "uid": "otherteam"},
    {"location": "someotherlocation", "store_type": "team", "uid": ""},
    {"location": "someotherlocation", "store_type": "user", "uid": ""},
]


@pytest.fixture(params=VALID_INPUTS)
def valid_store_data(tmp_path, request):
    """Fixture that yields mock store locations and types."""
    global_store_cache = tmp_path / "mbl-stores.json"
    store_dir = tmp_path / request.param["location"]
    _type = request.param["store_type"]
    uid = request.param["uid"]
    yield store_dir, _type, uid


@pytest.fixture(params=INVALID_INPUTS)
def invalid_store_data(tmp_path, request):
    """Fixture that yields mock store locations and types."""
    global_store_cache = tmp_path / "mbl-stores.json"
    store_dir = None
    _type = request.param["store_type"]
    uid = request.param["uid"]
    yield store_dir, _type, uid


class TestStore:
    """Test the store creation and discovery logic."""

    def test_store_created_correctly_with_valid_inputs(self, valid_store_data):
        """
        Test a Store is created and permissions are correct.

        Check the permissions for team and user stores
        are set to the correct values.
        Also assert that the store location file update function was called.
        """
        with mock.patch(
            "mbl.cli.utils.store._update_store_locations_file"
        ) as mock_slf:
            store_dir, store_type, uid = valid_store_data
            sf = store.create(
                uid=uid, location=store_dir, store_type=store_type
            )
            perms = oct(store_dir.stat().st_mode).replace("0o40", "0o")
            assert isinstance(sf, store.Store)
            if store_type == "user":
                assert perms == oct(0o700)
            else:
                assert perms == oct(0o755)
            assert sf.config_path.exists()
            mock_slf.assert_called_once_with(
                uid=uid, location=str(store_dir), store_type=store_type
            )

    def test_store_create__raises_with_invalid_inputs(
        self, invalid_store_data
    ):
        """
        Test a Store is created and permissions are correct.

        Check the permissions for team and user stores
        are set to the correct values.
        """
        with mock.patch(
            "mbl.cli.utils.store._update_store_locations_file"
        ) as mock_slf:
            store_dir, store_type, uid = invalid_store_data
            with pytest.raises((ValueError, IOError)):
                sf = store.create(
                    uid=uid, location=store_dir, store_type=store_type
                )
            mock_slf.assert_not_called()

    def test_global_store_record_is_updated(self, valid_store_data):
        """Test the file handler write function is called.
        Ensure called with the correct arguments."""
        with mock.patch("mbl.cli.utils.store.file_handler") as mock_fh:
            mock_fh.read_config_from_json.return_value = dict()
            store_dir, store_type, uid = valid_store_data
            sf = store.create(
                uid=uid, location=store_dir, store_type=store_type
            )
            mock_fh.write_config_to_json.assert_called_once_with(
                config_file_path=store.STORE_LOCATIONS_FILE_PATH,
                **{uid: str(store_dir)}
            )
