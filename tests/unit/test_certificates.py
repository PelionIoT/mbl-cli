# Copyright (c) 2019 Arm Limited and Contributors. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause


"""Tests for Pelion certificate management."""
import pathlib
import pytest

from unittest import mock
from mbl.cli.utils import store, cloudapi


VALID_CERT_NAMES = ["cert_a", "cert_b", "cert_c"]
INVALID_CERT_NAMES = ["blah", "invalid", "name"]

SRC_PATH = pathlib.Path(__file__).parent.absolute()


class CertID:
    id = "1"


class CertData:
    def __init__(self, name):
        self.header_file = (
            SRC_PATH / "mbed_cloud_dev_credentials.c"
        ).read_text()
        self.name = name


@pytest.fixture
def _mock_cert_api():
    with mock.patch(
        "mbl.cli.utils.cloudapi.CertificatesAPI", autospec=True
    ) as cert_api:
        cert_api.return_value.list_certificates.return_value = [
            CertID() for c in VALID_CERT_NAMES
        ]
        yield cert_api()


class TestDeveloperCertificates:
    @pytest.mark.parametrize("name", VALID_CERT_NAMES)
    def test_get_dev_credentials(self, name, _mock_cert_api):
        _mock_cert_api.get_certificate.return_value = CertData(name)
        dev_creds = cloudapi.DevCredentialsAPI("")
        assert isinstance(dev_creds.get_dev_credentials(name), dict)

    @pytest.mark.parametrize("name", INVALID_CERT_NAMES)
    def test_get_dev_credentials_invalid_cert_names(
        self, name, _mock_cert_api
    ):
        dev_creds = cloudapi.DevCredentialsAPI("")
        _mock_cert_api.get_certificate.return_value = CertData(
            VALID_CERT_NAMES[0]
        )
        with pytest.raises(ValueError):
            dev_creds.get_dev_credentials(name)

    def test_create_dev_credentials(self, _mock_cert_api):
        _mock_cert_api.add_developer_certificate.return_value = CertData(
            VALID_CERT_NAMES[0]
        )

        dev_creds = cloudapi.DevCredentialsAPI("")
        crt = dev_creds.create_dev_credentials("test_cert")
        assert isinstance(crt, dict)
