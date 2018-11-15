# Mbed Linux CLI
Command-line interface for developing with Mbed Linux

[![Circle CI](https://circleci.com/gh/ARMmbed/mbl-cli.svg?style=shield&circle-token=367893aefffecc72cf7d17201667cd2f75d6d5c7)](https://circleci.com/gh/ARMmbed/mbl-cli/)

The Mbed Linux CLI is a toolbox for managing target devices running Mbed Linux.

## Prerequisites

[Node.js > v8.10.0](https://nodejs.org), which includes `npm v3`

## Installation

The CLI is distributed using npm. To install the tool globally:

```bash
$ npm install -g ARMmbed/mbl-cli#build
```

## Usage

```bash
$ mbl-cli <command> [arguments]
```

### Options

- -v, --version - Show version number
- -h, --help - Show help

### Commands

#### Discovery and Select

Discover connected Mbed Linux devices and allow the user to select one for further commands.

```bash
$ mbl-cli select
```

#### Shell

Obtain a shell on a device, optionally specifying the device address to use

```
$ mbl-cli shell [address]
```

#### Run

Run a remote command on a device, optionally specifying the device address to use

```
$ mbl-cli run <command> [address]
```

#### Get

Copy a file from a device, optionally specifying the device address to use

```
$ mbl-cli get <src> <dest> [address]
```

#### Put

Copy a file to a device, optionally specifying the device address to use

```
$ mbl-cli put <src> <dest> [address]
```

#### Application Management

Application management commands.

```
$ mbl-cli app <command> [address]
```

_Commands:_

Start the application on a device.
```
$ mbl-cli app start [address]
```

Stop the application on a device.
```
$ mbl-cli app stop [address]
```

Restart the application on a device.
```
$ mbl-cli app restart [address]
```

## Implementation Status

- [x] discover and select a device
- [x] shell onto a device
- [x] run a remote command on a device
- [x] copy a file from/to a device
- [ ] deploy an application image on a device
- [ ] deploy a firmware component on a device
- [ ] start an application on a device
- [ ] stop an application on a device
- [ ] restart an application on a device
- [ ] configure the network for a device

## Development

Please refer to the [development documentation](DEVELOPMENT.md)
