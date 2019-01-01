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

### Commands

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


[mbl-license]: LICENSE.md
[mbl-contributing]: CONTRIBUTING.md
