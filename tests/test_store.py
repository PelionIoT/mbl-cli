#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Tests for the Store classes."""

from unittest import mock

import pytest
import pathlib
from mbl.cli.utils import store


@pytest.fixture(
    params=[
        {"location": "user", "store_type": "user", "uid": "rob"},
        {"location": "team", "store_type": "team", "uid": "dev-team"},
    ]
)
def valid_store_data(tmp_path, request):
    """Fixture that yields mock store locations and types."""
    store_dir = tmp_path / request.param["location"]
    _type = request.param["store_type"]
    uid = request.param["uid"]
    yield store_dir, _type, uid


@pytest.fixture(
    params=[
        {
            "location": str(pathlib.Path().home().resolve()),
            "store_type": "user",
            "uid": "rob",
        },
        {
            "location": str(pathlib.Path().home().resolve()),
            "store_type": "team",
            "uid": "new-team",
        },
    ]
)
def invalid_store_data(tmp_path, request):
    """Fixture that yields invalid mock store locations and types.

    The 'invalid' case is a location which already exists.
    """
    store_dir = request.param["location"]
    _type = request.param["store_type"]
    uid = request.param["uid"]
    yield store_dir, _type, uid


class TestStore:
    """Test the store creation and discovery logic."""

    def test_new_store_created_correctly_with_valid_inputs(
        self, valid_store_data
    ):
        """
        Test a Store is created and permissions are correct.

        Check the permissions for team and user stores
        are set to the correct values.
        Also assert that the store location file update function was called.
        """
        with mock.patch(
            "mbl.cli.utils.store.StoreLocationsRecord"
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
                assert perms == oct(0o750)
            assert sf.config_path.exists()
            mock_slf.return_value.update.assert_called_once_with(
                uid, str(store_dir)
            )

    def test_known_store_retrieved_correctly_with_valid_inputs(
        self, valid_store_data
    ):
        """
        Test a known store location is validated and permissions are correct.

        Check the permissions for team and user stores
        are set to the correct values.
        Also assert that the store location file update function was called.
        """
        with mock.patch("mbl.cli.utils.store.file_handler") as mock_fh:
            store_dir, _, uid = valid_store_data
            store_dir.mkdir(exist_ok=True)
            conf = store_dir / "config.json"
            conf.touch(exist_ok=True)
            mock_fh.read_config_from_json.return_value = {
                uid: str(store_dir.resolve()),
                "location": str(store_dir.resolve()),
            }

            sf = store.get(uid=uid)

            assert isinstance(sf, store.Store)
            assert sf.config_path.exists()

    def test_store_create_raises_with_invalid_inputs(self, invalid_store_data):
        """
        Test a Store is created and permissions are correct.

        Check the permissions for team and user stores
        are set to the correct values.
        """
        with mock.patch(
            "mbl.cli.utils.store.StoreLocationsRecord"
        ) as mock_slf:
            store_dir, store_type, uid = invalid_store_data

            with pytest.raises(IOError, match="The given path already exists"):
                store.create(
                    uid=uid, location=store_dir, store_type=store_type
                )

            mock_slf.update.assert_not_called()

    @pytest.mark.parametrize(
        "known_store_loc",
        [
            {"akakaka": "/docs/store"},
            {"rob": "askjdhksadhksdahkhasdkjhdsakjhjkdahashj"},
        ],
    )
    def test_store_get_raises_with_invalid_inputs(
        self, invalid_store_data, known_store_loc
    ):
        """
        Test a Store is created and permissions are correct.

        Check the permissions for team and user stores
        are set to the correct values.
        """
        with mock.patch("mbl.cli.utils.store.file_handler") as mock_fh:
            mock_fh.read_config_from_json.return_value = known_store_loc
            _, _, uid = invalid_store_data

            with pytest.raises(
                (
                    store.StoreNotFoundError,
                    store.KnownStoreLocationInvalid,
                    store.StoreConfigError,
                )
            ):
                store.get(uid=uid)

    def test_global_store_record_is_updated(self, valid_store_data):
        """Test the file handler write function is called.
        Ensure called with the correct arguments."""
        with mock.patch("mbl.cli.utils.store.file_handler") as mock_fh:
            mock_fh.read_config_from_json.return_value = dict()
            store_dir, store_type, uid = valid_store_data

            store.create(uid=uid, location=store_dir, store_type=store_type)

            mock_fh.write_config_to_json.assert_called_once_with(
                config_file_path=store.STORE_LOCATIONS_FILE_PATH,
                **{uid: str(store_dir)}
            )
