from mbed_cloud import CertificatesAPI


def create_developer_cert(api_key, name):
    cert_api = CertificatesAPI(
        dict(api_key=api_key)
    )
    certificate = cert_api.add_developer_certificate(
           name=name
        )
    return certificate.header_file