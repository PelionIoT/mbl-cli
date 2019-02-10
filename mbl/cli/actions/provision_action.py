from mbl.cli.utils.cloudapi import DevCredentialsAPI
from mbl.cli.utils.store import Store


def execute(args):
    cert_name = args.cert_name
    if args.create_cert:
        key_name = args.create_cert
        api_key = _retrieve_api_key_from_user_store(key_name)
        cert_data = _create_cert_from_api(api_key, cert_name)
        _save_credentials_to_team_store(cert_name, cert_data)
    else:
        cert_data = _get_cert_file_paths_from_team_store(cert_name)


def _retrieve_api_key_from_user_store(api_key_name):
    store_handle = Store("user")
    return store_handle.api_keys[api_key_name]


def _get_cert_file_paths_from_team_store(cert_name):
    sh = Store("team")
    return sh.dev_cert_data_files[cert_name]


def _create_cert_from_api(api_key, cert_name):
    credentials_api = DevCredentialsAPI(api_key)
    return credentials_api.create_dev_credentials(
        cert_name
    )


def _save_credentials_to_team_store(cert_name, cert_data):
    team_store_handle = Store("team")
    team_store_handle.add_developer_credentials(cert_name, cert_data)
    team_store_handle.save()
