#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Manage persistent storage locations used with device provisioning.

A "persistent storage location" consists of a directory on disk containing
a file named `config.json`. The persistent storage location is used to hold
credentials and certificates which are used to provision devices for use with
Pelion Device Management.
The `config.json` file holds information about the stored items and other
metadata (including paths to any objects in the persistent storage location
stored as files).
MBL-CLI also creates/accepts a file named `.mbl-stores.json`.
`.mbl-stores.json` is referred to as the STORE_LOCATIONS_FILE.
This is where known storage types and locations are saved as key/value pairs.

The `Store` class contained in this module provides the public interface to
access objects in a persistent storage location and save new items to the
store.
The `Store` class is basically a thin wrapper around a dict built from the
store's config.json.

* `Store` class representing a storage location on disk.
* `StoreLocationsRecord` class is an interface for STORE_LOCATIONS_FILE i/o.

Exceptions:
----
* `StoreNoteFoundError` Specified store location does not exist.
"""

import pathlib

from mbed_cloud import AccountManagementAPI

from . import file_handler

STORE_LOCATIONS_FILE_PATH = pathlib.Path().home() / ".mbl-stores.json"
DEFAULT_STORE_RECORD = {
    "user": str(pathlib.Path().home() / pathlib.Path(".mbl-store", "user")),
    "team":  str(pathlib.Path().home() / pathlib.Path(".mbl-store", "team"))
}


class Store:
    """This class is an abstraction of a storage location on disk.

    The store holds a `_config` dict. `_config` holds metadata
    about the store itself, and information on objects within the store.

    This object provides an interface to access the store config file data.
    """

    def __init__(self, store_type):
        """Build a store object from a path based on the store_type.

        The path_to_store on disk must exist before instantiating this class.

        :params str store_type: The type of store to build (team or user).
        """
        path_to_store = _get_or_create_store(store_type)
        self._config = file_handler.read_config_from_json(
            path_to_store / "config.json"
        )
        if not self._config:
            self._config = dict(
                location=str(path_to_store),
            )

    @property
    def api_keys(self):
        """Dict of all API keys held in the store.

        :returns dict: API keys in the form `{name: key, ...}`
        """
        return self._config.setdefault("api_keys", dict())

    @property
    def dev_certs(self):
        """Dict of all developer certificates held in the store.

        :returns dict: developer certs keys in the form `{name: cert, ...}`
        """
        return self._config.setdefault("dev_certs", dict())

    @property
    def config_path(self):
        """Path to the store config file."""
        return pathlib.Path(self._config["location"], "config.json")

    def save(self):
        """Save config data to a file."""
        file_handler.write_config_to_json(self.config_path, **self._config)

    def add_api_key(self, api_key):
        """Add an API key to the store.

        Query the Pelion API to validate the API key and retrieve its name.

        :param api_key str: The api key to add to the store.
        """
        api = AccountManagementAPI({"api_key": api_key})
        for known_api_key in api.list_api_keys():
            # The last 32 characters of the API key are 'secret'
            # and aren't included in the key returned by the api.
            if known_api_key.key == api_key[:-32]:
                self.api_keys[known_api_key.name] = api_key.strip()
                return
        raise ValueError("API key not recognised by Pelion.")


class StoreLocationsRecord:
    """Class represents the Store Locations Record.

    This class provides an interface to update and read the
    STORE_LOCATIONS_FILE.

    The store UIDs and locations in the STORE_LOCATIONS_FILE are held as JSON
    key-value pairs which map directly to this object's internal dictionary.
    """

    def __init__(self):
        """Initialise `_data` dict with data from STORE_LOCATIONS_FILE."""
        conf = file_handler.read_config_from_json(
            config_file_path=STORE_LOCATIONS_FILE_PATH
        )
        if not conf:
            file_handler.write_config_to_json(
                config_file_path=STORE_LOCATIONS_FILE_PATH,
                **DEFAULT_STORE_RECORD
            )
        self._data = conf if conf else DEFAULT_STORE_RECORD

    def update(self, store_type, location):
        """Write a new store UID and storage location to the record.

        Prevent setting a known UID's location.
        """
        self._data[store_type] = location
        file_handler.write_config_to_json(
            config_file_path=STORE_LOCATIONS_FILE_PATH, **self._data
        )

    def get(self, store_type):
        """Look up a store by UID and return the location.

        Verify the storage location is valid & exists on disk.
        :returns Path: file path to the storage location.
        """
        try:
            loc = pathlib.Path(self._data.get(store_type, None))
        except TypeError:
            raise StoreNotFoundError(
                "Store Type not recognised. Only User and Team supported."
            )
        return loc


class StoreNotFoundError(Exception):
    """The specified store does not exist."""


def _get_or_create_store(store_type):
    """Get the store path from the StoreLocationsRecord.

    Create the path if it doesn't exist.

    We expect the storage location and config.json to be automatically
    created in the scenario where a user is saving to the store for
    the first time.

    :param str store_type: type of store to get/create.
    """
    known_stores = StoreLocationsRecord()
    store_path = known_stores.get(store_type)
    mode = 0o700 if store_type == "user" else 0o750
    store_path.mkdir(mode=mode, parents=True, exist_ok=True)
    return store_path
