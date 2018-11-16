# Mbed Linux CLI

[![Circle CI](https://circleci.com/gh/ARMmbed/mbl-cli.svg?style=shield&circle-token=367893aefffecc72cf7d17201667cd2f75d6d5c7)](https://circleci.com/gh/ARMmbed/mbl-cli/)

[![Builds](https://img.shields.io/badge/mbed%20linux%20cli-builds-blue.svg)](http://armmbed.github.io/mbl-cli/builds/)

## Prerequisites

[Node.js > v8.10.0](https://nodejs.org), which includes `npm v3`.

## Latest Build

To install the latest development build:

```bash
$ npm install -g ARMmbed/mbl-cli#build
```

## Setup

After cloning this repository, install the npm dependencies:

```bash
$ npm install
```

## Building

Simply use the default ```gulp``` task to build the SDK and docs:

```bash
$ npm run gulp
```

## Watching

To continually watch for changes, use the gulp `watch` task:

```bash
$ npm run gulp watch
```

## Testing

Link the executable to make it globally available as `mbl-cli` by running:

```bash
$ npm link
```
