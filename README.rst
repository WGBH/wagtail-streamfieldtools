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
  - 3.4
  - 3.5

- `Wagtail <https://wagtail.io/>`_:

  - 1.2
  - 1.3
  - 1.4

.. note:: If you want to use Python 3.3 or Wagtail 1.1 install the 0.2 release.

Installation
------------

First, install with:

.. code-block:: bash

    $ pip install wagtail-streamfieldtools

After installation completes, add ``'streamfield_tools'`` to
``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        # All your other apps here
        'streamfield_tools',
    )

Running Tests
-------------

To run tests, first create a new virtual environment and install the test requirements:

.. code-block:: bash

    $ virtualenv TEST_ENV
    $ pip install -r test_requirements.txt

Then run the test suite with this command:

.. code-block:: bash

    $ coverage run --source streamfield_tools/ runtests.py

If all tests pass, then push your code to Github where Travis CI will tests against the entire dependency matrix. If [all tests passed there](https://travis-ci.org/WGBH/wagtail-streamfieldtools), then [head over to Coveralls](https://coveralls.io/github/WGBH/wagtail-streamfieldtools) to ensure your coverage has remained the same.

If the tests passed and coverage remained the same then it's time to release to PyPI!
