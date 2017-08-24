# transport

[![Build Status](https://travis-ci.org/adbpy/transports.svg?branch=master)](https://travis-ci.org/adbpy/transports)
[![Test Coverage](https://codeclimate.com/github/adbpy/transports/badges/coverage.svg)](https://codeclimate.com/github/adbpy/transports/coverage)
[![Code Climate](https://codeclimate.com/github/adbpy/transports/badges/gpa.svg)](https://codeclimate.com/github/adbpy/transports)
[![Issue Count](https://codeclimate.com/github/adbpy/transports/badges/issue_count.svg)](https://codeclimate.com/github/adbpy/transports)

[![Stories in Ready](https://badge.waffle.io/adbpy/transports.svg?label=ready&title=Ready)](http://waffle.io/adbpy/transports)

Android Debug Bridge (ADB) Transports

## Status

This project is actively maintained and under development.

## Installation

To install transports from [pip](https://pypi.python.org/pypi/pip):
```bash
    $ pip install adbts
```

To install transports from source:
```bash
    $ git clone git@github.com:adbpy/transports.git
    $ cd transports && python setup.py install
```

## Goals/Scope

A standalone library that can be used for providing multiple communication transports within the context of ADB.
The transport project should care about:

* Synchronous vs. Asynchronous constructs
* Communications transports such as TCP, UDP, and USB

The transports project should not care about:

* Byte layout on the wire
* High level constructs such as connection "handshakes"
* Cryptography required to verify endpoints
* Anything else not explicitly mentioned above...

## Contributing

If you would like to contribute, simply fork the repository, push your changes and send a pull request.
Pull requests will be brought into the `master` branch via a rebase and fast-forward merge with the goal of having a linear branch history with no merge commits.

## License

[Apache 2.0](LICENSE)
