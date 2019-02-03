#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Manage persistent storage locations used with device provisioning.

A "persistent storage location" consists of a directory on disk where objects
are stored as files.
This directory contains a file named `config.json` which contains
some metadata about the store and any stored items (including paths to any
files in the persistent storage location).
MBL-CLI also creates a file named `.mbl-stores.json`.
`.mbl-stores.json` is referred to as STORE_LOCATIONS_FILE.
This is where known storage UIDs and locations are saved as key/value pairs.

The `Store` class contained in this module is basically a thin wrapper
for the dict passed to its `__init__` method as the `metadata` parameter.
`metadata` is built from data in a store's `config.json` file by either the
`get` or `create` functions (which must be used to create a `Store` instance.
This is explained further below).
`Store` provides an interface to access objects in a persistent storage
location and save new items to the store.

To instantiate a `Store` use the `get` or `create` functions.
`get` will retrieve the `config.json` data from a known persistent storage
location.
A `Store` object wrapping this data is then instantiated and returned.
`create` will create a new persistent storage location on disk
before instantiating a `Store` object and returning it.
The `get` and `create` functions also perform some validation checks
on the store metadata and file paths.

* `get` factory function gets a path to a persistent storage location from
 a known UID and builds a `Store` instance from the config.json.
* `create` factory function creates a new persistent storage location and
builds a `Store` instance from the function's input parameters.
* `Store` class representing a storage location on disk.
* `StoreLocationsRecord` class is an interface for STORE_LOCATIONS_FILE i/o.

Exceptions:
----
* `StoreNotFoundError` store UID is unknown.
* `KnownStoreLocationInvalid` known store UID has no known path on disk.
* `StoreConfigError` existing store config.json contains no data.
"""

import pathlib

from . import file_handler

STORE_LOCATIONS_FILE_PATH = pathlib.Path().home() / ".mbl-stores.json"
DEFAULT_USER_STORE_NAME = "default-user"
DEFAULT_TEAM_STORE_NAME = "default-team"


def create(uid, store_type, location):
    """Create a new store on disk and return a `Store` instance.

    Create the store directory and config file with the correct permissions.

    Update the StoreLocationsRecord with the new store's uid & location.
    Pack the store metadata into a dictionary and wrap it in a `Store` object.

    :params str uid: store's UID.
    :params str location: path to the store.
    :params str store_type: type of store (user or team).
    :returns `Store`: A `Store` object.
    """
    mode = 0o700 if store_type == "user" else 0o750
    path_to_store = pathlib.Path(location)
    config_file_path = path_to_store / "config.json"
    try:
        path_to_store.mkdir(parents=True, mode=mode)
        config_file_path.touch(mode=mode)
    except FileExistsError:
        raise IOError("The given path already exists.")
    metadata = dict(
        uid=uid, location=str(path_to_store.resolve()), store_type=store_type
    )
    # Add the new store uid and location to the record.
    StoreLocationsRecord().update(uid, metadata["location"])
    return Store(metadata)


def get(uid):
    """Build a `Store` from an existing store config file on disk.

    Find the known store config file based on the store's UID in the
    `StoreLocationsRecord`.
    Read store metadata from the config file and wrap it in a `Store` object.

    :params str uid: store's UID.
    :returns `Store`: A `Store` object.
    """
    if uid.lower() in [DEFAULT_USER_STORE_NAME, DEFAULT_TEAM_STORE_NAME]:
        # Implicitly create the default store if it doesn't exist.
        # The user has elected to `get` the default `Store`,
        # and expects the directory and config to be automatically created.
        path_to_store = _get_or_create_default_store(uid)
    else:
        # Query the known stores record.
        path_to_store = StoreLocationsRecord().get(uid)
    metadata = file_handler.read_config_from_json(
        path_to_store / "config.json"
    )
    if not metadata:
        raise StoreConfigError(
            "The config file at {} contains no data. "
            "Your store is corrupt, please delete and recreate.".format(
                path_to_store
            )
        )
    return Store(metadata)


class Store:
    """This class is an abstraction of a storage location on disk.

    The store holds a `_config` dict. `_config` holds metadata
    about the store itself, and information on objects within the store.

    This object provides an interface to access the store config file data.

    NOTE: You usually won't instantiate this object directly. Instead use the
    `get` or `create` factory functions.
    """

    def __init__(self, metadata):
        """Create a `Store` object.

        :params dict metadata: Store metadata from the store config file.
        """
        self._config = metadata

    @property
    def api_keys(self):
        """List of API keys held in the store."""
        return self._config.setdefault("api_keys", list())

    @property
    def config_path(self):
        """Path to the store config file."""
        return pathlib.Path(self._config["location"], "config.json")

    def save(self):
        """Save config data to a file."""
        file_handler.write_config_to_json(self.config_path, **self._config)


class StoreLocationsRecord:
    """Class represents the Store Locations Record.

    This class provides an interface to stream data to/from the
    STORE_LOCATIONS_FILE.

    The store uids and locations in the STORE_LOCATIONS_FILE are held as JSON
     key-value pairs which map directly to this object's internal dictionary.
    """

    def __init__(self):
        """Initialise `UserDict.data` with data from STORE_LOCATIONS_FILE."""
        self._data = file_handler.read_config_from_json(
            config_file_path=STORE_LOCATIONS_FILE_PATH
        )

    def update(self, uid, location):
        """Write a new store UID and storage location to the record.

        Prevent setting a known UIDs location.
        """
        if uid not in self._data:
            self._data[uid] = location
            file_handler.write_config_to_json(
                config_file_path=STORE_LOCATIONS_FILE_PATH, **self._data
            )
        else:
            raise KeyError(
                "Trying to add a store UID that already exists in the record."
            )

    def get(self, uid):
        """Get a known store's UID from the record.

        Verify the storage location is valid & exists on disk.
        :returns Path: file path to the storage location.
        """
        try:
            loc = pathlib.Path(self._data.get(uid, None))
        except TypeError:
            raise StoreNotFoundError(
                "UID not recognised. You must create a store."
            )
        if not loc.exists():
            # We've found a 'known store' that doesn't actually exist on disk.
            # Delete from the store locations record and raise an exception.
            del self._data[uid]
            file_handler.write_config_to_json(
                config_file_path=STORE_LOCATIONS_FILE_PATH, **self._data
            )
            raise KnownStoreLocationInvalid(
                "A 'known store' location does not exist on disk."
                " You must recreate the store."
            )
        return loc


class StoreNotFoundError(Exception):
    """The specified store does not exist."""


class KnownStoreLocationInvalid(Exception):
    """A store UID is associated with a path that does not exist."""


class StoreConfigError(Exception):
    """Store config file exists but contains no data."""


def _get_or_create_default_store(uid):
    """Get the default store path, creating it if it doesn't exist.

    This 'create' aspect of this covers the case when a user is saving to the
    default store for the first time.
    We expect the default storage location and config.json to be automatically
    created in this scenario.

    :param str: UID for this default store (team & user have independent UIDs)
    :return Path: path to the default store.
    """
    default_sp = pathlib.Path().home() / ".mbl-store/{}".format(uid)
    if not default_sp.exists():
        # default store type is in the UID
        stype = uid.split("-")[1].strip()
        default_sp.mkdir()
        file_handler.write_config_to_json(
            config_file_path=default_sp / "config.json",
            **dict(
                uid=uid, location=str(default_sp.resolve()), store_type=stype
            )
        )
    return default_sp
