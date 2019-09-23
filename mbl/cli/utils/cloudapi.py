#!/usr/bin/env python3
# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""Wrappers for the mbed-cloud-sdk."""

import array

from mbed_cloud import AccountManagementAPI, CertificatesAPI
from mbed_cloud.exceptions import CloudApiException


def valid_api_key(api_key):
    """Call the Pelion Account Management API to validate an API key.

    :param str api_key: API key to validate.
    """
    api = AccountManagementAPI({"api_key": api_key})
    try:
        # We need to make a call to the api for the key to be validated.
        api.get_account()
    except CloudApiException:
        return False
    return True


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
            self._cert_api.get_certificate(c.id).name
            for c in self._cert_api.list_certificates()
        ]

    def get_dev_credentials(self, name):
        """Get an existing developer certificate from Pelion.

        Return a credentials object.

        :param str name: name of the developer certificate to create.
        """
        for cert in self._cert_api.list_certificates():
            this_cert = self._cert_api.get_certificate(cert.id)
            if this_cert.name == name:
                return _parse_cert_header(
                    this_cert.header_file,
                    "#include <inttypes.h>",
                    "MBED_CLOUD_DEV_",
                )
        raise ValueError(
            "The developer certificate does not exist. "
            "Available certificates: \n{}".format(
                "\n".join(self.existing_cert_names)
            )
        )

    def create_dev_credentials(self, name):
        """Create a new developer certificate and return a credentials object.

        :param str name: name of the developer certificate to create.
        """
        try:
            cert = self._cert_api.add_developer_certificate(name=name)
            return _parse_cert_header(
                cert.header_file, "#include <inttypes.h>", "MBED_CLOUD_DEV_"
            )
        except CloudApiException as err:
            if err.reason != "Conflict":
                raise
            raise ValueError(
                "The developer certificate you are trying to create "
                "already exists in the Pelion Device Management Portal."
            )

    def delete_developer_certificate(self, name):
        """Delete an existing developer certificate from device management."""
        for cert in self._cert_api.list_certificates():
            if cert.name == name:
                self._cert_api.delete_certificate(cert.id)
                return
        raise ValueError(
            "Certificate '{}' was not found in Device Management.".format(name)
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

    `match_str_pre` is used to split the include statements from the
    header body. It should be the last preprocessor statement at the top
    of the header. (`match_str_pre` is passed directly to str.find. This is
    not a RE!)

    `match_str_var` is used to match the variable names (all variables in
    these certs have a consistent naming scheme, `match_str_var` is passed
    directly to str.find. This is not a RE!)

    :param str cert_header: The certificate header to parse.
    :param str match_str_pre: The last preprocessor statement to split on.
    :param str match_str_var: The variable match to find.

    :return dict: credentials object
    """
    cert_header = cert_header.strip()
    _, body = cert_header.split(match_str_pre)
    cpp_statements = body.split(";")
    out_map = dict()
    for statement in cpp_statements:
        statement = statement.replace("\n", "")
        # skip statements that aren't var assignments
        if "=" not in statement:
            continue
        var_name_and_type, raw_val = statement.split(" = ")
        # ignore sizeof variables
        if "sizeof(" in raw_val:
            continue
        # slice out the variable type before the name
        var_name_begin = var_name_and_type.find(match_str_var)
        if var_name_begin is -1:
            raise ValueError("{} var match not found.".format(match_str_var))
        processed_name = (
            var_name_and_type[var_name_begin:].replace(r"[]", "").strip()
        )
        # remove unwanted characters from the variable value string.
        # if replace or strip fail they do it silently, so this covers
        # all the "unwanted character" cases in these headers.
        processed_value = (
            raw_val.replace(r" '", "")  # 'c' -> c
            .replace(r'"', "")  # "bootstrapServer" -> bootstrapServer
            .replace(" ", "")  # 0x7f_ -> 0x7f (_ represents whitespace)
            .strip(r"{} \r")  # {0x7f}\r -> 0x7f
        )
        # try to split on commas, the resulting list will be of length 1
        # if this value is a single string or int. If it's an array then
        # we'll get a list with len > 1.
        values = processed_value.split(",")
        if len(values) > 1:
            # is an array of hexadecimal values
            fmt_arr = [int(av, 16) for av in values]
            out_val = array.array("B", fmt_arr).tobytes()
        else:
            # is a single string or int/uint value
            out_val = values[0].encode()
        out_map[processed_name] = out_val
    return out_map
