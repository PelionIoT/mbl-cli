# Mbed Linux OS CLI

## Prerequisites

[Python > v3.6](https://python.org) and `pip`. 

It's recommended to use a venv for development.

## Latest Build

Clone the repository

```bash
$ git clone git@github.com:ARMmbed/mbl-cli.git
```

## Setup

After cloning the repository install the dev dependencies:

```bash
$ cd /path/to/repo
$ pip install -r requirements.txt
```
This will install dependencies and install the mbl-cli in 'editable' mode.

## Testing

If you installed into a venv, make sure to activate it, this will add mbl-cli to the PATH.

If you installed mbl-cli to your system python it will already be on PATH.

Since the requirements.txt instructed pip to install the tool in editable mode, it will automatically pick up any code changes.

```bash
$ mbl-cli <command>
```

Run the unit tests in a docker container.

```bash
cd mbl-cli/tests
./run-tests.sh
```