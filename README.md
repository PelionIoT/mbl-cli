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

MBL-CLI provides support for dynamically injecting mcc credentials in to devices.

Persistent storage for Pelion Cloud Credentials is also provided using the tool.

#### Persistent Storage

It is possible to save Pelion Cloud Credentials to either a 'Developer Store' or 'Team Store' depending on the given context.

* Developer Store: only accessible by a single user or member of the administrators group. This is where developer API keys are stored.
* Team Store: accessible by all groups. This is the storage location for the firmware update authority certificate, used to sign firmware update manifests.

You can optionally specify a location for the Developer Store and/or Team Store. The MBL-CLI will use the following defaults:
* Default location for the Developer Store is `~/.mbl-cli/dev-store/` (Permissions for this folder are set to drw-------)
* Default location for shared storage in the Team Store is `~/.mbl-cli/team-store/` (Permissions for this folder are set to drw-rw----)

It is possible to have multiple Developer and Team Stores, referenced by UID.

The user must provide a UID/name to associate with the Developer Store or Team Store location on first use.
The UID/name provided is used by the mbl-cli to reference the appropriate store.

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
