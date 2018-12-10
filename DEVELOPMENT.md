# Mbed Linux OS CLI

## Prerequisites

[Python > v3.6](https://python.org) and `pip`. 

It's recommended to use [pipenv](https://github.com/pypa/pipenv) to install into a venv and manage package dependencies. A `Pipfile` and `Pipfile.lock` are included to facilitate pipenv usage.

## Latest Build

Clone the repository

```bash
$ git clone git@github.com:ARMmbed/mbl-cli.git
```

## Setup

After cloning the repository install the dev dependencies (assuming you have pipenv installed):

```bash
$ cd /path/to/repo
$ pipenv install --dev
```
This will create a virtual environment, install dependencies and install the mbl-cli in 'editable' mode.

## Testing

Enable the pipenv shell to activate the virtual environment.

```bash
$ cd /path/to/repo
$ pipenv shell
```

Now mbl-cli can be invoked.

```bash
$ mbl-cli <command>
```

Run the unit tests in a docker container.

```bash
cd mbl-cli/tests
./run-tests.sh
```

