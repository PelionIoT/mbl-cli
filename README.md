# Mbed Linux OS CLI
Command-line interface for developing with Mbed Linux OS


The Mbed Linux OS CLI is a toolbox for managing target devices running Mbed Linux OS.


## License

Please see the [License][mbl-license] document for more information.


## Contributing

Please see the [Contributing][mbl-contributing] document for more information.


## Prerequisites

[Python > v3.6](https://python.org) and `pip`. 


## Installation

The CLI is distributed using pypi. To install the tool use `pip`

```bash
$ pip install mbl-cli
```

## Usage

```bash
$ mbl-cli <command> [arguments]
```

### Options

- -h, --help - Show help

### Help

Show help for a specific command

```bash
$ mbl-cli <command> -h, --help
```

### Basic Commands

#### Discovery and Select

Discover connected Mbed Linux OS devices and allow the user to select one for further commands.

```bash
$ mbl-cli select
```

#### Discovery and List

Discover connected Mbed Linux OS devices and show a list of the hostnames.

```bash
$ mbl-cli list
```

#### Shell

Obtain a shell on a device, optionally specifying the device IPv4/IPv6 address to use

```bash
$ mbl-cli [address] shell 
```

#### Run a Single Command

Run a remote command on a device, optionally specifying the device IPv4/IPv6 address to use

```bash
$ mbl-cli [address] shell <command>
```

#### Get

Copy a file from a device, optionally specifying the device IPv4/IPv6 address to use

```bash
$ mbl-cli [address] get <src> <dest> 
```

#### Put

Copy a file to a device, optionally specifying the device IPv4/IPv6 address to use

```bash
$ mbl-cli [address] put <src> <dest>
```

### Device Provisioning

During development, you don't need to go through the full factory process every time you want to test a device or a software version.

Pelion Device Management offers a developer mode to speed up the development process. The mode relies on a developer certificate that you can add to your software binary. The developer certificate allows your test device to connect to your Device Management account.

You can use the same certificate on up to 100 devices. If you need more test devices, you will need to generate a second certificate.

When updating the firmware on a device you must upload a signed [firmware manifest](https://cloud.mbed.com/docs/current/updating-firmware/firmware-manifests.html) to the Pelion cloud. MBL-CLI also provides functionality to create a public/private keypair used to sign the firmware update manifest.

Pelion provide several REST APIs relating to device management. The API keys to authenticate with the Pelion REST APIs are created on the Pelion website. The API keys must be stored locally to be repeatedly accessible. After viewing the API key on initial creation, it is no longer fully visible in the Pelion portal.

MBL-CLI provides support for dynamically injecting Pelion developer certificates into devices.

Persistent storage for Pelion API keys, firmware update authority certificates and developer certificates is also provided using the tool.

#### Persistent Storage

It is possible to save Pelion Cloud Credentials to either a 'Developer Store' or 'Team Store' depending on the given context.

* Developer Store: only accessible by a single user or member of the administrators group. This is where developer API keys are stored. This will usually be a location on your dev machine, used for quick access to Pelion API keys the MBL-CLI will use for further provisoning activities.
* Team Store: accessible by all groups. This is the storage location for the firmware update authority certificate for a device. This certificate is used to sign firmware update manifests. The Team Store would generally be set to a location accessible by your team (for example a cloud share).

You can optionally specify a location for the Developer Store and/or Team Store. The MBL-CLI will use the following defaults:
* Default location for the Developer Store is `~/.mbl-cli/dev-store/` (Permissions for this folder are set to drwx------)
* Default location for shared storage in the Team Store is `~/.mbl-cli/team-store/` (Permissions for this folder are set to drwxrw----)

It is possible to have multiple Developer and Team Stores, referenced by UID.

The user must provide a UID/name to associate with the Developer Store or Team Store location on first use.
The UID/name provided is used by the MBL-CLI to reference the appropriate store.

### Device Provisioning Commands

#### SaveApikey

Store a Pelion Cloud API key in the specified developer storage location.

```bash
$ mbl-cli save-api-key <uid> <api-key> [store-location]
```

#### CreateUpdateCert

This command will generate an X.509 keypair then create and sign a public key certificate used to sign update manifests. [More information here](https://cloud.mbed.com/docs/v1.3/updating-firmware/update-auth-cert.html). The public key certificate is saved in the Team Store.

If no Team Store location exists, then you will be prompted to create one.

```bash
$ mbl-cli create-update-cert <uid>
```

[mbl-license]: LICENSE.md
[mbl-contributing]: CONTRIBUTING.md
