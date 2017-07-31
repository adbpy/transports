# transport-protocol

[![Build Status](https://travis-ci.org/adbpy/transport-protocol.svg?branch=master)](https://travis-ci.org/adbpy/transport-protocol)
[![Test Coverage](https://codeclimate.com/github/adbpy/transport-protocol/badges/coverage.svg)](https://codeclimate.com/github/adbpy/transport-protocol/coverage)
[![Code Climate](https://codeclimate.com/github/adbpy/transport-protocol/badges/gpa.svg)](https://codeclimate.com/github/adbpy/transport-protocol)
[![Issue Count](https://codeclimate.com/github/adbpy/transport-protocol/badges/issue_count.svg)](https://codeclimate.com/github/adbpy/transport-protocol)

[![Stories in Ready](https://badge.waffle.io/adbpy/transport-protocol.svg?label=ready&title=Ready)](http://waffle.io/adbpy/transport-protocol)

Android Debug Bridge (ADB) Transport Protocol

## Status

This project is actively maintained and under development.

## Installation

To install transport-protocol from [pip](https://pypi.python.org/pypi/pip):
```bash
    $ pip install adbtp
```

To install transport-protocol from source:
```bash
    $ git clone git@github.com:adbpy/transport-protocol.git
    $ cd transport-protocol && python setup.py install
```

## Goals/Scope

A standalone library that can be used for providing multiple communication transports within the context of ADB.
The transport protocol should care about:

* Synchronous vs. Asynchronous constructs
* Network transports such as TCP, UDP, and USB

The transport protocol should not care about:

* Byte layout on the wire
* High level constructs such as connection "handshakes"
* Cryptography required to verify endpoints
* Anything else not explicitly mentioned above...

## Contributing

If you would like to contribute, simply fork the repository, push your changes and send a pull request.
Pull requests will be brought into the `master` branch via a rebase and fast-forward merge with the goal of having a linear branch history with no merge commits.

## License

[Apache 2.0](LICENSE)