#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Tests for the Store classes."""

import pathlib
from unittest import mock

import pytest

from mbl.cli.utils import store


@pytest.fixture(
    params=[
        {"location": "", "store_type": "user", "uid": "default"},
        {"location": "", "store_type": "team", "uid": "default"},
        {"location": "user", "store_type": "user", "uid": "rob"},
        {"location": "team", "store_type": "team", "uid": "dev-team"},
        {"location": "", "store_type": "user", "uid": "otheruser"},
        {"location": "", "store_type": "team", "uid": "otherteam"},
        {"location": "someotherlocation", "store_type": "team", "uid": ""},
        {"location": "someotherlocation", "store_type": "user", "uid": ""},
    ]
)
def store_data(tmp_path, request):
    """Fixture that yields mock store locations and types."""
    global_store_cache = tmp_path / "mbl-stores.json"
    store_dir = tmp_path / request.param["location"]
    location_param = request.param["location"]
    store_config = store_dir / "config.json"
    store_type = request.param["store_type"]
    uid = request.param["uid"]
    yield store_dir, store_config, store_type, uid, location_param


class TestStore:
    """Test the store creation and discovery logic."""

    def test_store_permissions_set_correctly(self, store_data):
        """
        Test Store Permissions are correct.

        Check the permissions for team and user stores
        are set to the correct values.
        """
        store_dir, store_config, store_type, uid, location_param = store_data
        sf = store.StoreFinder(
            uid=uid, location=store_dir, store_type=store_type
        )
        if self._is_compatible_parameter_set(uid, location_param):
            loc = sf.get_or_create_location()
            assert oct(loc.stat().st_mode).replace("0o40", "0o") == oct(
                sf.permissions
            )
        else:
            try:
                assert sf.get_or_create_location()
            except (ValueError, IOError):
                assert True

    def test_store_locations_and_configs_are_found_or_created(
        self, store_data
    ):
        """Test store configs are discovered or created."""
        store_dir, store_config, store_type, uid, location_param = store_data
        sf = store.StoreFinder(
            uid=uid, location=store_dir, store_type=store_type
        )
        if self._is_compatible_parameter_set(uid, location_param):
            assert sf.get_or_create_location().resolve() == store_dir.resolve()
        else:
            try:
                assert sf.get_or_create_location()
            except (ValueError, IOError):
                assert True

    def test_global_store_record_is_updated(self, store_data):
        """Test the global store cache is updated."""
        with mock.patch("mbl.cli.utils.store.file_handler") as mock_fh:
            mock_fh.read_known_stores.return_value = dict()
            store_dir, store_config, store_type, uid, location_param = (
                store_data
            )
            sf = store.StoreFinder(
                uid=uid, location=store_dir, store_type=store_type
            )
            if self._is_compatible_parameter_set(uid, location_param):
                sf.update_global_store_record(uid=uid, location=location_param)
                mock_fh.write_store_config.assert_called_once_with(
                    **{uid: location_param}
                )

    def _is_compatible_parameter_set(self, uid, location):
        """Check if we should be raising due to incompatible parameters."""
        if uid and (not location):
            return False
        else:
            return True
