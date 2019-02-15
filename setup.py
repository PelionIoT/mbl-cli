#!/usr/bin/env python3
# Copyright (c) 2018 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Setuptools entry point."""

from setuptools import setup, find_packages
import os


def read(file_name):
    """Read a file, return the contents as a str."""
    with open(file_name, "r") as readme:
        return readme.read()


setup(
    name="mbl-cli",
    version="2.0.0",
    description="Mbed Linux OS Command Line Tool",
    long_description=read("README.md"),
    author="Arm Ltd.",
    license="BSD-3-Clause",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "paramiko>=2.4.2",
        "scp>=0.13.0",
        "zeroconf>=0.21.3",
        "mbed-cloud-sdk>=2.0.4",
        "cryptography==2.4.2",
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["mbl-cli = mbl.cli.mbl_cli:_main"]},
)
