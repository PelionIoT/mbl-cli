from mbl.cli.utils import certificates
from mbl.cli.utils.store import Store


def execute(args):
    cert_name = args.cert_name
    if args.create_cert:
        key_name = args.create_cert
        store_handle = Store("user")
        api_key = store_handle.api_keys[key_name]
        cert_header = certificates.create_developer_cert(api_key, cert_name)
        parsed = certificates.parse_cert_header(cert_header)
        team_store_handle = Store("team")
        team_store_handle.dev_certs[cert_name] = parsed
        team_store_handle.save()
    else:
        sh = Store("team")
        cert_header = sh.dev_certs[cert_name]
        print(cert_header)