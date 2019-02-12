#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Wrappers for the mbed-cloud-sdk."""

from mbed_cloud import CertificatesAPI, AccountManagementAPI
from mbl.cli.utils import file_handler


def find_api_key_name(api_key):
    """Query the Pelion API to retrieve an API key's name.

    :param str api_key: full API key to find the name of.
    :raises ValueError: if the API key isn't found.
    """
    api = AccountManagementAPI({"api_key": api_key})
    for known_api_key in api.list_api_keys():
        # The last 32 characters of the API key are 'secret'
        # and aren't included in the key returned by the api.
        if known_api_key.key == api_key[:-32]:
            return known_api_key.name
    raise ValueError("API key not recognised by Pelion.")


class DevCredentialsAPI:
    """API to manage developer certificate creation.

    Wrap the CertificatesAPI. Creates/gets and parses developer certificates.
    """

    def __init__(self, api_key):
        """Initialise the API."""
        self._cert_api = CertificatesAPI(dict(api_key=api_key))

    @property
    def existing_cert_names(self):
        """List all existing certificate names known to the Pelion account."""
        return [
            self._cert_api.get_certificate(c["id"]).name
            for c in self._cert_api.list_certificates()
        ]

    def get_dev_credentials(self, name):
        """Get an existing developer certificate from Pelion.

        Return a credentials object.

        :param str name: name of the developer certificate to create.
        """
        for c in self._cert_api.list_certificates():
            this_cert = self._cert_api.get_certificate(c["id"])
            if this_cert.name == name:
                return _parse_cert_header(
                    this_cert.header_file,
                    "#include <inttypes.h>",
                    "MBED_CLOUD_DEV_"
                )
        raise ValueError(
            "The developer certificate does not exist."
            "Available certificates: \n{}".format(
                "\n".join(self.existing_cert_names)
            )
        )

    def create_dev_credentials(self, name):
        """Create a new developer certificate and return a credentials object.

        :param str name: name of the developer certificate to create.
        """
        cert = self._cert_api.add_developer_certificate(name=name)
        return _parse_cert_header(
            cert.header_file, "#include <inttypes.h>", "MBED_CLOUD_DEV_"
        )


def parse_existing_update_cert(update_cert_header_path):
    """Open an existing certificate file and push it through the parser."""
    with open(update_cert_header_path) as hfile:
        update_cert_header = hfile.read()
    return _parse_cert_header(
        update_cert_header, "#include <stdint.h>", "arm_uc_"
    )


def _parse_cert_header(cert_header, match_str_pre, match_str_var):
    """Parse a certificate header.

    Store the data as key/value pairs (variable name/value) in a
    dictionary.

    match_str_pre is used to split the include statements from the
    header body. It should be the last preprocessor statement at the top
    of the header.
    match_str_var is used to match the variable names (all variables in
    these certs have a consistent naming scheme, match_str_var is passed
    directly to str.find. This is not a RE!)

    :param str cert_header: The certificate header to parse.
    :param str match_str_pre: The last preprocessor statement to split on.
    :param str match_str_var: The variable match to find.

    :return dict: credentials object
    """
    cert_header = cert_header.strip()
    _, body = cert_header.split(match_str_pre)
    print(_, body)
    cpp_statements = body.split(";")
    out_map = dict()
    for statement in cpp_statements:
        statement = statement.replace("\n", "")
        # skip preprocessor directives
        if statement.startswith("#"):
            continue
        var_name, val = statement.split(" = ")
        # sanitise the string tokens
        var_pp_name = var_name[var_name.find(match_str_var) :].replace(
            r"[]", ""
        )
        val_pp = val.replace(r" '", "").replace(r'"', "").replace(",", "\n").strip(r"{} ")
        out_map[var_pp_name] = val_pp
    return out_map
