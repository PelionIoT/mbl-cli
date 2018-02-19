# Mbed Linux CLI
Command-line interface for developing with Mbed Linux

[![Circle CI](https://circleci.com/gh/ARMmbed/mbed-linux-cli.svg?style=shield&circle-token=367893aefffecc72cf7d17201667cd2f75d6d5c7)](https://circleci.com/gh/ARMmbed/mbed-linux-cli/)

The Mbed Linux CLI is a toolbox for building your Mbed Linux applications and managing them on your target device.

## Prerequisites

[Docker > v17.0.0](https://www.docker.com)

[Node.js > v6.0.0](https://nodejs.org), which includes `npm`

## Installation

The CLI is distributed using npm. To install the tool globally:

```bash
$ npm install -g ARMmbed/mbed-linux-cli#build
```

## Usage

```bash
$ mbed-linux <command> [arguments]
```

### Commands

Build a directory and create an image:
```bash
$ mbed-linux build [directory] [file]
```

Deploy a directory or image to a device:
```
$ mbed-linux deploy [path] [address]
```

Device management commands:
```
$ mbed-linux device <command> [address]
```

### Options

- -v, --version - Show version number
- -h, --help - Show help

These commands can be used to build applications in the [example applications](https://github.com/ARMMbed/mbed-linux-cli/tree/master/example_apps/) directory

## Implementation Status

- [x] build locally
- [x] build remotely
- [x] deploy to a device
- [x] start an application on a device
- [x] stop a application on a device
- [x] restart an application on a device
- [x] get logs from a device
- [ ] discover devices
- [ ] configure a device
- [ ] ssh to a device

## Development

Please refer to the [development documentation](DEVELOPMENT.md)
