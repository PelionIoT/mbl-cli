# Mbed Linux OS CLI

Command-line interface for developing with Mbed Linux OS

The Mbed Linux OS CLI is a toolbox for managing target devices running Mbed Linux OS.

## License

Please see the [License][mbl-license] document for more information.

## Contributing

Please see the [Contributing][mbl-contributing] document for more information.


## Prerequisites

[Python > v3.5](https://python.org) and `pip`. 


## Installation

The CLI is distributed using pypi. To install the tool use `pip`

```bash
pip install mbl-cli
```

## Usage

```bash
mbl-cli <command> [arguments]
```

### Options

- -h, --help - Show help

### Help

Show help for a specific command

```bash
mbl-cli <command> -h, --help
```

### Commands

#### Discovery and Select

Discover connected Mbed Linux OS devices and allow the user to select one for further commands.

```bash
mbl-cli select
```

#### Discovery and List

Discover connected Mbed Linux OS devices and show a list of the hostnames.

```bash
mbl-cli list
```

#### Shell

Obtain a shell on a device, optionally specifying the device IPv4/IPv6 address to use

```bash
mbl-cli [address] shell 
```

#### Run a Single Command

Run a remote command on a device, optionally specifying the device IPv4/IPv6 address to use

```bash
mbl-cli [address] shell <command>
```

#### Get

Copy a file from a device, optionally specifying the device IPv4/IPv6 address to use

```bash
mbl-cli [address] get <src> <dest> 
```

#### Put

Copy a file to a device, optionally specifying the device IPv4/IPv6 address to use

```bash
mbl-cli [address] put <src> <dest>
```

#### SaveApikey

Store a Pelion Service API key.

API keys are saved in the User Store. MBL-CLI will also query the Pelion Service API the name given to the key when it was created. The name is stored alongside the key.

```bash
mbl-cli save-api-key <api-key>
```

#### ProvisionPelion

Create a developer certificate and inject it into the target device.

This command will instruct MBL-CLI to perform the following actions.

- Obtain or create a developer certificate and update certificate.
- Inject the certificates into the selected device's secure storage.

 MBL-CLI will search the Team Store for a device certificate if the `--create-dev-cert` option is omitted. If `--create-dev-cert` is given, MBL-CLI will create a new certificate using the Pelion Service API, provision the device, and store the certificate in your Team Store for later use.

```bash
mbl-cli provision-pelion <dev-cert-name> <update-default-resources-path> [--create-dev-cert]
```

#### CreateUpdateCert

This command will generate an X.509 keypair then create and sign a public key certificate used to sign update manifests. The certificate is saved in your Team Store.

```bash
mbl-cli create-update-cert
```

### Device Provisioning Support

To connect your devices to Pelion Device Management, you must provision the device with security credentials that establish trust with the cloud services.

During development, you don't need to go through the full factory provisioning process every time you want to test a device or a software version.

Pelion Device Management offers a developer mode to speed up the development process. This mode relies on a developer certificate. The developer certificate allows your test device to connect to your Device Management account. Developer certificates are used to establish trust between the device and a Pelion Device Management account.

You can use the same certificate on up to 100 devices. You can generate another certificate if you need to provision more devices.

Previously the developer certificate had to be added to your Mbed Linux OS build configuration.
Now you can provision your devices dynamically at runtime using the MBL-CLI.

To update the firmware on a device you must upload a signed [firmware manifest](https://cloud.mbed.com/docs/current/updating-firmware/firmware-manifests.html) to the Pelion cloud.

An update authority certificate is used to sign the firmware update manifest. The manifest is then uploaded to Pelion Device Management and can be used to initiate a firmware update campaign. MBL-CLI will accept an update certificate created with the `manifest-tool` and use this to provision your device. MBL-CLI also provides a command to create an update authority certificate. [More information on the update authority certificate](https://cloud.mbed.com/docs/current/updating-firmware/update-auth-cert.html).

Pelion provides several REST APIs relating to device management. The API keys used to authenticate with the Pelion APIs are created in the Pelion Device Management portal. MBL-CLI requires use of an API key to perform provisioning activities.

MBL-CLI defines persistent storage locations on your developer machine for Pelion API keys, firmware update authority certificates and developer certificates. This storage feature helps to simplify the provisioning workflow and allow easier authentication with Pelion APIs.

#### Persistent Storage

It is possible to save Pelion Cloud credentials to either a 'User Store' or 'Team Store' depending on the context of the object being saved.

These stores are located on your developer machine at locations you can optionally specify.

- User Store: This is where per user Pelion API keys are stored.
- Team Store: This is where developer certificates and firmware update authority certificates for your devices are stored.

The Team Store can be set to a location accessible by your team (for example a cloud share). If your team then specify this location for their Tema Store config (see below) they can use the CLI tool to access the device certificates to provision other devices.

To specify a storage location you must provide a config file `~/.mbl-stores.json` with the following contents:

```json
{
    "user": path/to/user/store,
    "team": path/to/team/store
}
```

The MBL-CLI will use the following defaults if no config is given:

- Default location for the User Store is `~/.mbl-store/user/` (Permissions for this folder are set to drwx------). Owning user is the *nix user who created the store (the store is automatically created on first use).
- Default location for shared storage in the Team Store is `~/.mbl-store/team/` (Permissions for this folder are set to drwxrw----). You should set this store's user:group according to access permissions you have defined for your team.

The defaults will be saved to `~/.mbl-stores.json` after first use, where they can be edited if required.

#### Developer Provisioning Workflow

The developer provisioning workflow consists of the following steps:

- Obtain a developer certificate from the Pelion Device Management service.
- Inject the certificate into secure storage on the target device.

To inject a developer certificate into your device using MBL-CLI, follow the steps below.

NOTE: This tutorial assumes you have already created a `update_default_resources.c` file using the `manifest-tool` as described [here](https://os.mbed.com/docs/mbed-linux-os/v0.5/getting-started/preparing-device-management-sources.html#creating-an-update-resources-file).

Connect your Mbed Linux device to your development PC. Run the `select` command.
The select command will return a list of discovered devices, you can select your device by its list index.

```bash
$ mbl-cli select
Discovering devices. This will take up to 30 seconds.

1: mbed-linux-os-9999: fe80::21b:63ff:feab:e6a6%enpos623

$ 1

```

Obtain an API key from the Pelion Device Management website. Copy the API key to your clipboard when prompted on the website.

Store your API key using the following command (replacing `<api-key>` with the real API key in your clipboard). This command validates the key exists in the Pelion Cloud. It then saves the key in the User Store.

MBL-CLI will automatically choose the first API key it finds in the User Store when it requires authentication with the Pelion APIs.

```bash
mbl-cli save-api-key <api-key>
```

Run the provisioning command.

```bash
mbl-cli provision-pelion  <cert-name> <update-cert-path> --create-dev-cert
```

This command will provision your selected device with the developer and update certificates. You must pass in a name for your developer certificate and the path to the `update_default_resources.c` file created using the manifest-tool. Because we passed in `--create-dev-cert` MBL-CLI will create a new developer certificate with the given name, then save it in the Team Store for use with other devices. If we had omitted this option, MBL-CLI would search the Team Store for a dev certificate with the given name. After obtaining the certificates, MBL-CLI will inject it into your selected device's secure storage.

[mbl-license]: LICENSE.md
[mbl-contributing]: CONTRIBUTING.md
