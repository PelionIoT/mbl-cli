# Mbed Linux OS CLI

## Prerequisites

[Python > v3.6](https://python.org) and `pip`. 

It's recommended to use a virtual environment for development.

Create a virtual environment using venv

```bash
$ python -m venv /path/to/venv
```

Activate the virtual environment you just created

```bash
$ source /path/to/venv/bin/activate
```

## Latest Build

Clone the repository

```bash
$ git clone git@github.com:ARMmbed/mbl-cli.git
```

## Setup

Install the dev dependencies into your active virtual environment

```bash
$ cd /path/to/repo
$ pip install -r requirements.txt
```

This will also install the mbl-cli in 'editable' mode (i.e pip install -e).

## Usage

The tool can be invoked when your virtual environment is active

```bash
$ mbl-cli <command>
```

Since we installed mbl-cli in editable mode, it will watch for any code changes.

## Testing

Run the unit tests using pytest

```bash
pytest -vvv
```