#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Tests for the Store classes."""

from unittest import mock

import pytest
from mbl.cli.utils import store


class TestStore:
    @pytest.mark.parametrize("store_type", ["user", "team"])
    def test_store_instantiation(self, store_type):
        """Test the file handler write function is called.
        Ensure called with the correct arguments."""
        with mock.patch("mbl.cli.utils.store.file_handler") as mock_fh:
            mock_fh.from_json.return_value = dict()
            store.Store(store_type=store_type)
            expected_p = store.StoreLocationsRecord.STORE_LOCATIONS_FILE_PATH
            mock_fh.to_json.assert_called_once_with(
                config_file_path=expected_p, **store.DEFAULT_STORE_RECORD
            )

    @pytest.mark.parametrize("store_type", ["blah", "b;aha;;a;"])
    def test_store_raises_on_invalid_type(self, store_type):
        """Test the file handler write function is called.
        Ensure called with the correct arguments."""
        with mock.patch("mbl.cli.utils.store.file_handler") as mock_fh:
            mock_fh.from_json.return_value = dict()
            with pytest.raises(store.StoreNotFoundError):
                store.Store(store_type=store_type)
