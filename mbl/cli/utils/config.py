#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Storage config objects."""


import json
import os
from collections import namedtuple
from . import file_handler


def make_store_config(**conf_data):
    """Create a namedtuple from a store config file.

    :param dict conf_data: Dictionary of config file items.
    """
    fields_ = " ".join(conf_data.keys())
    return namedtuple("StoreConfig", fields_)(**conf_data)
