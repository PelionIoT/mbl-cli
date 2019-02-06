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

### Basic Commands

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

### Device Provisioning

During development, you don't need to go through the full factory process every time you want to test a device or a software version.

Pelion Device Management offers a developer mode to speed up the development process. The mode relies on a developer certificate that you can add to your software binary. The developer certificate allows your test device to connect to your Device Management account.

You can use the same certificate on up to 100 devices. If you need more test devices, you will need to generate a second certificate.

MBL-CLI provides support for dynamically provisioning your device with a developer certificate.

When updating the firmware on a device you must upload a signed [firmware manifest](https://cloud.mbed.com/docs/current/updating-firmware/firmware-manifests.html) to the Pelion cloud. MBL-CLI also provides functionality to create a public/private keypair used to sign the firmware update manifest.

Pelion provides several REST APIs relating to device management. The API keys used to authenticate with the Pelion REST APIs are created in the Pelion Device Management portal. The API keys must be stored locally to be repeatedly accessible. After viewing the API key on initial creation, it is no longer fully visible in the Pelion portal.

Persistent storage on your developer machine for Pelion API keys, firmware update authority certificates and developer certificates is also provided; this helps to simplify the provisioning workflow and allow easier authentication with Pelion REST APIs.

#### Persistent Storage

It is possible to save Pelion Cloud credentials to either a 'Developer Store' or 'Team Store' depending on the given context.
These stores are located on your developer machine at a location you specify. It is recommended to set the Team Store location to a shared folder that your team can access.

- Developer Store: only accessible by a single user. This is where developer API keys are stored. This store is used for quick access to Pelion API keys the MBL-CLI will use for further provisioning activities.
- Team Store: group accessible (provided your team has access to the Team Store folder on your developer machine or cloud share). This is the storage location for the firmware update authority certificate for a device. This certificate is used to sign firmware update manifests. The Team Store would generally be set to a location accessible by your team (for example a cloud share).

You can optionally specify to create a new Developer Store or Team Store. The MBL-CLI will use the following defaults:

- Default location for the Developer Store is `~/.mbl-cli/default-user/` (Permissions for this folder are set to drwx------)
- Default location for shared storage in the Team Store is `~/.mbl-cli/default-team/` (Permissions for this folder are set to drwxrw----)

The user must provide a UID to associate with the Developer Store or Team Store location.
The UID provided is given by the user on subsequent uses of the tool to access a store.

### Device Provisioning Commands

#### SaveApikey

Store one or more Pelion Cloud API keys in the specified storage location.
Multiple API keys can be given as and they'll be added to the store.
Optionally specify `--new-store` when saving to a new storage location.
If `--new-store` is passed, it must be given a set of `INFO` arguments.
The arguments always required by `INFO` are `PATH` and a `CONTEXT`:
If `CONTEXT` is `team` then `USER` and `GROUP` must also be given.

The `INFO` arguments must be given in the following order.

- `PATH` path to the new store location
- `CONTEXT` team or user store.
- `USER` set the store's user (required if `CONTEXT` is `team`)
- `GROUP` set the store's group (required if `CONTEXT` is `team`)

```bash
mbl-cli save-api-key <uid> <api-key...> [--new-store PATH CONTEXT [USER GROUP]]
```

#### CreateUpdateCert

This command will generate an X.509 keypair then create and sign a public key certificate used to sign update manifests. [More information here](https://cloud.mbed.com/docs/current/updating-firmware/update-auth-cert.html). The public key certificate is saved in the Team Store.

If no Team Store location exists, then you will be prompted to create one.

```bash
mbl-cli create-update-cert <uid>
```

[mbl-license]: LICENSE.md
[mbl-contributing]: CONTRIBUTING.md
