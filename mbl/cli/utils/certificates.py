from mbed_cloud import CertificatesAPI
from mbl.cli.utils import store


def create_developer_cert(name):
    store_handle = store.get("default-user")
    conf = {"api_key": store_handle.api_keys["dev"]}
    cert_api = CertificatesAPI(conf)
    cert_data = {
        "name": name
    }
    certificate = cert_api.add_developer_certificate(
            **cert_data
        )
    print(certificate)
