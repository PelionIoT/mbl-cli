#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Pytest configuration file."""


def pytest_report_teststatus(report):
    """Override Pytest hook to report test status."""
    if report.when == "call":
        if report.passed:
            lava = "<LAVA_SIGNAL_TESTCASE TEST_CASE_ID={} RESULT=pass>".format(
                report.nodeid.replace(" ", "_")
            )
            return report.outcome, "*", lava

    if report.failed:
        lava = "<LAVA_SIGNAL_TESTCASE TEST_CASE_ID={} RESULT=fail>".format(
            report.nodeid.replace(" ", "_")
        )
        return report.outcome, "*", lava


def pytest_addoption(parser):
    parser.addoption("--address")
