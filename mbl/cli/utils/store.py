#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Manage persistent storage locations.

Instantiate a `Store` using the `get` or `create` functions. 
These factory functions perform some validation checks on the store metadata
and file paths before returning a `Store` instance.

The `Store` class wraps a dictionary of metadata and paths to stored objects.
The dictionary is created from a `config.json` file in an existing storage
location on disk, or the input arguments if creating a new store.

`Store` provides an interface to access
objects in storage and save items to the store.

* `get` factory function creates a `Store` from a known UID.
* `create` factory function creates a `Store`, \
new store directory and config file paths.
* `Store` class representing a storage location on disk.

Exceptions:
* `StoreNotFoundError` store UID is unknown.
* `KnownStoreLocationInvalid` known store UID has no known path on disk.
* `StoreConfigError` existing store config.json contains no data.
"""


from . import file_handler
import pathlib


STORE_LOCATIONS_FILE_PATH = pathlib.Path().home() / ".mbl-stores.json"
DEFAULT_USER_STORE_NAME = "default-user"
DEFAULT_TEAM_STORE_NAME = "default-team"


def create(uid, store_type, location):
    """Create a new store on disk and return a `Store` instance.

    Create the store directory and config file with the correct permissions.

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
    _update_store_locations_file(**metadata)
    return Store(metadata)


def get(uid):
    """Get existing store metadata from a known config file, return a `Store`.

    Find the known config file based on the store UID.
    Read store metadata from the config file and wrap it in a `Store` object.

    :params str uid: store's UID.
    :returns `Store`: A `Store` object.
    """
    if uid.lower() in [DEFAULT_USER_STORE_NAME, DEFAULT_TEAM_STORE_NAME]:
        path_to_store = pathlib.Path().home() / ".mbl-store/{}".format(uid)
    else:
        path_to_store = _get_existing_store_path_from_uid(uid)
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


class StoreNotFoundError(Exception):
    """The specified store does not exist."""


class KnownStoreLocationInvalid(Exception):
    """A store UID is associated with a path that does not exist."""


class StoreConfigError(Exception):
    """Store config file exists but contains no data."""


class Store:
    """This class is an abstraction of a storage location on disk.

    The store holds a `_config` dict. `_config` holds metadata
    about the store itself, and information on objects within the store.

    This object provides an interface to access the store config file data.

    NOTE: You usually won't instantiate this object directly. Instead use the
    `get` or `create` module level convenience functions.
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


def _update_store_locations_file(**store_conf):
    """Update the store locations file with the new store details."""
    known_stores = file_handler.read_config_from_json(
        config_file_path=STORE_LOCATIONS_FILE_PATH
    )
    if store_conf and store_conf["uid"] not in known_stores:
        known_stores.update({store_conf["uid"]: store_conf["location"]})
        file_handler.write_config_to_json(
            config_file_path=STORE_LOCATIONS_FILE_PATH, **known_stores
        )


def _get_existing_store_path_from_uid(uid):
    known_stores = file_handler.read_config_from_json(
        config_file_path=STORE_LOCATIONS_FILE_PATH
    )
    try:
        loc = pathlib.Path(known_stores.get(uid, None))
    except TypeError:
        raise StoreNotFoundError(
            "UID not recognised. You must create a store."
        )
    if not loc.exists():
        # We've found a 'known store' that doesn't actually exist on disk.
        # Delete from the store locations record and raise an exception.
        del known_stores[uid]
        file_handler.write_config_to_json(
            config_file_path=STORE_LOCATIONS_FILE_PATH, **known_stores
        )
        raise KnownStoreLocationInvalid(
            "A 'known store' location does not exist on disk."
            " You must recreate the store."
        )
    else:
        return loc
