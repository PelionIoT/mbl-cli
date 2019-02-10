from mbed_cloud import CertificatesAPI, AccountManagementAPI


def find_api_key_name(api_key):
    """Query the Pelion API to retrive an API key's name.

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
    """Create a developer credentials object from the CertificatesAPI.

    Wrap the CertificatesAPI and use it to manage developer certificates.
    """
    def __init__(self, api_key):
        self._cert_api = CertificatesAPI(
            dict(api_key=api_key)
        )

    @property
    def existing_cert_names(self):
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
                return self._parse_cert_header(this_cert.header_file)
        raise ValueError(
            "The developer certificate does not exist."
            "Available certificates are: {}".format(
                "\n".join(self.existing_cert_names)
                )
            )

    def create_dev_credentials(self, name):
        """Create a new developer certificate and return a credentials object.

        :param str name: name of the developer certificate to create.
        """
        cert = self._cert_api.add_developer_certificate(
           name=name
        )
        return self._parse_cert_header(cert.header_file)

    def _parse_cert_header(self, cert_header):
        """Parse the certificate header.

        Store the data as key/value pairs (variable name/value) in a
        dictionary.

        :return dict: credentials object
        """
        cert_header = cert_header.strip()
        _, body = cert_header.split("#include <inttypes.h>")
        cpp_statements = body.split(";")
        out_map = dict()
        for statement in cpp_statements:
            statement = statement.replace("\n", "")
            # skip preprocessor directives
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
