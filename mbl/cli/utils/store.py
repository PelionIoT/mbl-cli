#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Manage persistent storage."""


from . import file_handler
import pathlib


STORE_LOCATIONS_FILE_PATH = pathlib.Path().home() / ".mbl-stores.json"


class Store:
    """This class is an abstraction of a storage location on disk.

    The store holds a config dict which holds metadata
    about objects in the store.

    This object is a thin wrapper around the config which
    provides an interface to access the objects held in the store.
    """

    def __init__(self, uid, store_type, location, **store_data):
        """Create a Store object and ensure the path exists on the filesystem.

        Check if the Store is already known by looking up its uid
        in the store locations file. If known get the path from the file.

        If the uid is unknown we're creating a new store. In this case fall
        back to the given location.
        Create the location if it doesn't already exist in the filesystem.

        Fill a params dictionary with config data from either
        a store's actual config file, or the input args if it doesnt exist.

        :params str uid: store's uid.
        :params str store_type: type of store (user or team)
        :params str location: Path to the store.
        :params dict store_data: Paths to objects or API keys the store holds.
        """
        if location is not None:
            path_to_store = _create_new_storage_location(
                location, mode=0o700 if store_type == "user" else 0o755
            )
        else:
            path_to_store = _get_store_location(uid, store_type)
        self._config = file_handler.read_config_from_json(
            path_to_store.resolve() / "config.json"
        )
        if not self._config:
            self._config = dict(
                uid=uid,
                location=str(path_to_store.resolve()),
                store_type=store_type,
                **store_data
            )
        _update_store_locations_file(**self._config)

    @property
    def api_keys(self):
        """List of API keys held in the store."""
        return self._config["api_keys"]

    @property
    def config_path(self):
        """Path to the store config file."""
        return pathlib.Path(self._config["location"], "config.json")

    def add_api_keys(self, api_keys):
        """Add a list of API keys to the store."""
        for api_key in list(api_keys):
            if api_key not in self.api_keys:
                self.api_keys.append(api_key)

    def save(self):
        """Save config data to a file."""
        file_handler.write_config_to_json(
            STORE_LOCATIONS_FILE_PATH, **self._config
        )


def _default_store_path(store_type):
    """Path to the default storage location."""
    sp = pathlib.Path().home() / ".mbl-store/default-{}".format(store_type)
    return sp


def _update_store_locations_file(**store_conf):
    """Update the store locations file with the new store details."""
    known_stores = file_handler.read_config_from_json(
        config_file_path=STORE_LOCATIONS_FILE_PATH
    )
    if store_conf["uid"] not in known_stores:
        known_stores.update({store_conf["uid"]: store_conf["location"]})
        file_handler.write_config_to_json(
            config_file_path=STORE_LOCATIONS_FILE_PATH, **known_stores
        )


def _get_store_location(uid, store_type):
    """Access the known stores and retrieve the storage location."""
    known_stores = file_handler.read_config_from_json(
        config_file_path=STORE_LOCATIONS_FILE_PATH
    )
    if uid.lower() == "default":
        path_object = _default_store_path(store_type)
    else:
        path_object = _get_store_path_from_uid(uid, known_stores)
    return path_object


def _create_new_storage_location(location, mode):
    """Create a new storage location."""
    path_object = pathlib.Path(location)
    location.mkdir(parents=True, exist_ok=True, mode=mode)
    return path_object


def _get_store_path_from_uid(uid, known_stores):
    try:
        loc = known_stores[uid]
    except KeyError:
        raise StoreNotFoundError()
    else:
        return pathlib.Path(loc)


class StoreNotFoundError(Exception):
    """The specified store location does not exist."""
