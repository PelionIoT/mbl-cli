#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Manage persistent storage."""


from . import file_handler
import pathlib


STORE_LOCATIONS_FILE_PATH = pathlib.Path().home() / ".mbl-stores.json"


def create(uid, store_type, location, **kwargs):
    """Create a Store object and ensure the path exists on the filesystem.

    Check if the Store is already known by looking up its uid
     in the store locations file. If known get the path from the file.

    If the uid is unknown we're creating a new store. In this case fall
     back to the given location.
    Create the location if it doesn't already exist in the filesystem.

    Fill a params dictionary with config data from either
    a store's actual config file, or the input args if it doesnt exist.

    :param str uid: The unique identifier of the store.
    :param str location: The path to the store.
    :param dict kwargs: Any other data to write to persistent storage.
    :returns Store: A Store object.
    """
    if uid.lower() == "default":
        location = _default_store_path(store_type)
    else:
        try:
            location = _get_store_path_from_uid(uid)
        except StoreNotFoundError:
            if location is not None:
                location = pathlib.Path(location)
            else:
                raise IOError(
                    "Unknown store uid and no location given."
                )
    if not location.exists():
        location.mkdir(
            parents=True,
            exist_ok=True,
            mode=0o700 if store_type == "dev" else 0o755
        )
    params = file_handler.read_config_from_json(
        location.resolve() / "config.json"
    )
    if not params:
        params = dict(
            uid=uid,
            location=str(location.resolve()),
            store_type=store_type,
            **kwargs
        )
    _update_store_locations_file(**params)
    return Store(**params)


class Store:
    """This class is an abstraction of a storage location on disk,
    which holds credential objects for use with
    device management.

    This object wraps a dictionary,
    providing an interface to access the objects held in the store.
    """

    def __init__(self, **data):
        """Initialise a Store object.

        :params dict data: all objects and metadata in the store.
        """
        self._config = data

    @property
    def api_keys(self):
        """List of API keys held in the store."""
        return self._config["api_keys"]

    @property
    def config(self):
        """Access the config dict directly."""
        return self._config

    @property
    def config_path(self):
        """Path to the store config file."""
        return pathlib.Path(self._config["location"], "config.json")

    def add_all_api_keys(self, api_keys):
        """Add a list of API keys to the store."""
        for api_key in list(api_keys):
            if api_key not in self.api_keys:
                self.api_keys.append(api_key)


def _default_store_path(store_type):
    """Path to the default storage location."""
    sp = pathlib.Path().home() / ".mbl-store/default-{}".format(
        store_type
    )
    return sp


def _update_store_locations_file(**store_conf):
    """Update the store locations file with the new store details."""
    known_stores = file_handler.read_config_from_json(
        config_file_path=STORE_LOCATIONS_FILE_PATH
    )
    if store_conf["uid"] not in known_stores:
        known_stores.update(
            {store_conf["uid"]: store_conf["location"]}
        )
        file_handler.write_config_to_json(
            config_file_path=STORE_LOCATIONS_FILE_PATH, **known_stores
        )


def _get_store_path_from_uid(uid):
    """Access the known stores and retrieve the storage location."""
    known_stores = file_handler.read_config_from_json(
        config_file_path=STORE_LOCATIONS_FILE_PATH
    )
    try:
        loc = known_stores[uid]
    except KeyError:
        raise StoreNotFoundError()
    else:
        return pathlib.Path(loc)


class StoreNotFoundError(Exception):
    """The specified store location does not exist."""
