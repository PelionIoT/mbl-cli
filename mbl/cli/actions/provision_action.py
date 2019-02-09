from mbl.cli.utils import certificates
from mbl.cli.utils.store import Store


def execute(args):
    if args.create_cert:
        key_name, cert_name = args.create_cert
        store_handle = Store("user")
        api_key = store_handle.api_keys[key_name]
        cert = certificates.create_developer_cert(api_key, cert_name)
        team_store_handle = Store("team")
        team_store_handle.dev_certs[cert_name] = cert
        team_store_handle.save()