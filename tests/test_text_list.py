#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Text list tests."""

import re
import sys

import pytest

from mbl.cli.utils import text_list


@pytest.fixture(params=[("blah", "haha", "jajaja"), ()])
def _text_list(request):
    """Create TextList with all args in params."""
    the_list = text_list.IndexedTextList()
    for p in request.param:
        the_list.append(p)
    yield the_list


class TestTextList:
    """TextList tests."""

    def test_item_can_be_added(self, _text_list):
        """Check an item is added to the list."""
        initial_len = len(_text_list.data)
        _text_list.append("yep")
        assert len(_text_list.data) > initial_len

    def test_list_formatted_correctly(self, _text_list):
        """Check the formatting is correct."""
        for index, returned_item in enumerate(_text_list):
            assert "{}".format(index + 1) in returned_item
            assert re.match(r"[0-9]\: [a-zA-Z]*", returned_item) is not None
