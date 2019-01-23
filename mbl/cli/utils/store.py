#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Manage persistent storage."""


from . import config
from . import file_handler
import pathlib


def init(uid, store_type, location=str(), **kwargs):
    """Initialise an existing store or create a new one.

    Populate the StoreConfig struct with config data.
    :param str uid: The unique identifier of the store to create.
    """
    store_finder = StoreFinder(uid, location, store_type)
    location = store_finder.get_or_create_location()
    conf_path = store_finder.get_config_file_path()
    if not conf_path.exists():
        params = dict(
            uid=uid,
            location=str(location.resolve()),
            store_type=store_type,
            **kwargs
        )
    else:
        params = file_handler.JSONParser(conf_path).from_file()
    store_config = config.make_store_config(**params)
    store_finder.update_global_store_record(
        uid=store_config.uid, location=store_config.location
    )
    return Store(store_config)


class Store:
    """Represents a storage location."""

    def __init__(self, conf_object):
        """Initialse the store.

        :params StoreConfig conf_object: A store configuration.
        """
        self.conf = conf_object

    @property
    def api_keys(self):
        """List of API keys held in the store."""
        return self.conf.api_keys

    @property
    def config(self):
        """Access the StoreConfig object directly."""
        return self.conf

    @property
    def config_path(self):
        """Path to the store config file."""
        return pathlib.Path(self.conf.location, "config.json")

    def add_all_api_keys(self, api_keys):
        """Add a list of API keys to the store."""
        for api_key in list(api_keys):
            if api_key not in self.api_keys:
                self.api_keys.append(api_key)


class StoreFinder:
    """Find and manage storage locations."""

    def __init__(self, uid, location, store_type):
        """Initialse the StoreFinder.

        :params uid: Storage unique identifier.
        :params location: Path to the physical storage location on disk.
        :params store_type: Type of storage being referenced (Team or User).
        """
        self.known_stores = file_handler.read_known_stores()
        self.location = location
        self.uid = uid
        self.store_type = store_type
        self.permissions = (
            0o755 if self.store_type.lower() == "team" else 0o700
        )

    def get_or_create_location(self):
        """Find a storage location, or create one if it doesn't exist."""
        if self.uid.lower() == "default":
            if self.location:
                raise ValueError(
                    "You provided the UID for default store."
                    " You don't need to specify a location!"
                )
            self.location = self._default_store()
        else:
            try:
                self.location = self._get_store_location()
            except StoreNotFoundError as err:
                if not self.location:
                    raise IOError(
                        "Null or invalid storage location given."
                    ) from err
                self.location = pathlib.Path(self.location)
        if not self.location.exists():
            self.location.mkdir(parents=True, mode=self.permissions)
        return self.location

    def get_config_file_path(self):
        """Return the path to the store config file."""
        return self.location.resolve() / "config.json"

    def update_global_store_record(self, **store_conf):
        """Update the global store cache with the new store details."""
        if store_conf["uid"] not in self.known_stores:
            self.known_stores.update(
                {store_conf["uid"]: store_conf["location"]}
            )
            file_handler.write_store_config(**self.known_stores)

    def _get_store_location(self):
        """Access the known stores and retrieve the storage location."""
        try:
            loc = self.known_stores[self.uid]
        except KeyError:
            raise StoreNotFoundError(
                "UID is unknown."
                " Your store either does not exist or is unknown to mbl-cli."
            )
        else:
            return pathlib.Path(loc)

    def _default_store(self):
        """Path to the default storage location."""
        sp = pathlib.Path().home() / ".mbl-store/default-{}".format(
            self.store_type
        )
        sp.mkdir(parents=True, exist_ok=True, mode=self.permissions)
        return sp


class StoreNotFoundError(Exception):
    """The specified store location does not exist."""
