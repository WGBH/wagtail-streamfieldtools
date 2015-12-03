========================
wagtail-streamfieldtools
========================

.. image:: https://travis-ci.org/WGBH/wagtail-streamfieldtools.svg?branch=master
    :target: https://travis-ci.org/WGBH/wagtail-streamfieldtools
    :alt: Travis CI Status

.. image:: https://coveralls.io/repos/WGBH/wagtail-streamfieldtools/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/WGBH/wagtail-streamfieldtools?branch=master
    :alt: Coverage Percentage

.. image:: https://img.shields.io/pypi/dm/wagtail-streamfieldtools.svg?style=flat
    :target: https://pypi.python.org/pypi/wagtail-streamfieldtools/
    :alt: Downloads

.. image:: https://img.shields.io/pypi/v/wagtail-streamfieldtools.svg?style=flat
    :target: https://pypi.python.org/pypi/wagtail-streamfieldtools/
    :alt: Latest Version


A suite of tools that extends `Wagtail <https://wagtail.io/>`_'s already-awesome `StreamField <http://docs.wagtail.io/en/latest/topics/streamfield.html>`_ to make it even more flexible/versatile/useful!

Includes:

- A simple interface for displaying the individual blocks of a ``StreamField`` in any number of renditions.
- A 'block registry' (and its associated field, ``RegisteredBlockStreamField``) that makes blocks pluggable/re-usable across disparate models/apps/projects.

Compatibility
-------------

- Python:

  - 2.7
  - 3.3
  - 3.4

- `Wagtail <https://wagtail.io/>`_:

  - 1.1
  - 1.2

TODO:

- Docs (with useful, easy-to-follow examples)!
