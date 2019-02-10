from mbed_cloud import CertificatesAPI


def create_developer_cert(api_key, name):
    cert_api = CertificatesAPI(
        dict(api_key=api_key)
    )
    certificate = cert_api.add_developer_certificate(
           name=name
        )
    return certificate.header_file


def parse_cert_header(cert_header):
    cert_header = cert_header.strip()
    _, body = cert_header.split("#include <inttypes.h>")
    cpp_statements = body.split(";")
    out_map = dict()
    for statement in cpp_statements:
        statement = statement.replace("\n", "")
        if statement.startswith("#"):
            continue
        var_name, val = statement.split(" = ")
        # sanitise the string tokens
        var_pp_name = var_name[var_name.find("MBED_CLOUD_DEV_"):].replace(
                r"[]", ""
            )
        val_pp = val.replace(r" '", "").replace(r'"', "").strip(r"{} ")
        out_map[var_pp_name] = val_pp
    return out_map
