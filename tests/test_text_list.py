#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from mbl.cli.utils import print_list
import sys


@pytest.fixture(params=[("blah", "haha", "jajaja"), ()])
def text_list(request):
    yield print_list.TextList(request.param)


class TestTextList:
    def test_item_can_be_added(self, text_list):
        initial_len = len(text_list.data)
        text_list.add("yep")
        assert len(text_list.data) > initial_len

    def test_list_formatted_correctly(self, text_list):
        ret = text_list.show()
        for index, (returned_item, list_data) in enumerate(
            zip(ret, text_list.data)
        ):
            assert returned_item == f"{index+1}: {list_data}"