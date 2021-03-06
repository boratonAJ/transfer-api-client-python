NOTE: This package is no longer being updated, use the
`Globus SDK for Python <http://globus.github.io/globus-sdk-python/>`_
instead.

This package contains an client library for the Globus Transfer API.

For detailed documentation of the Transfer API, see
`https://docs.globus.org/api/transfer/ <https://docs.globus.org/api/transfer/>`_

Installation
============

If you downloaded the source from github, simply run:

::

    python setup.py install

There is also a package on PyPI with the latest stable version; it can
be installed with ``easy_install`` or ``pip``:

::

    easy_install globusonline-transfer-api-client

Usage
=====

Basic usage:

::

    from globusonline.transfer import api_client

    api = api_client.TransferAPIClient(username="myusername",
                                    cert_file="/path/to/client/credential",
                                    key_file="/path/to/client/credential")
    status_code, status_message, data = api.task_list()

See the ``globusonline/transfer/api_client/examples`` directory for more
complete examples. If you installed from PyPI, this will be somewhere in
your Python path:

::

    python -c "from globusonline.transfer import api_client; print api_client.__path__"

One of the best ways to learn the library is to run an interactive
interpreter with an instance of the client. The module provides a
shortcut for doing this:

::

    python -i -m globusonline.transfer.api_client.main USERNAME -p
    >>> status_code, status_message, data = api.task_list()
    >>> dir(api) # get a list of all available methods

replace USERNAME with your Globus Online username, and you will be
prompted for your password.

Changelog
=========

0.10.18
-------

- Use standard python httplib if the python version has PEP 0476 (2.7.9+).
  This should fix an issue with using an http proxy, since the custom
  verified_https library uses private APIs that broke in later versions of
  2.7.x.

0.10.17
-------

- Remove deprecated 'bearer' authentication method.
- Remove deprecated method 'task_subtask_list'.

0.10.16
-------

- Add method for creating shared endpoints.
- Add method for successful transfers API to replace subtask API.
- Add methods for new server API.

0.10.15
-------

- Add InCommon CA and simplify CA handling.
- Improve handling of HTML errors.

0.10.14
-------

- Handle 503 errors within retry loop.
- Replace GO abbreviation in prompts with Globus Online.

0.10.13
-------

- Add goauth authentication and remove cookie authentication. Password
  prompt now uses goauth instead of scraping a cookie from the website.
- Add hostname validation to verified_https module.
- Add missing options to endpoint_create.
- Add example add-endpoint.py that prompts for username and password and
  uses goauth to authenticate.

0.10.12
-------

-  Fix password prompt authentication to work with current globusonline
   website.
-  Support keyword args to ``Transfer`` constructor; can be used to pass
   ``encrypt_data``, ``verify_checksum``, and any options added in the
   future, without requiring a client library update.
-  Support Bearer auth header for passing the auth token in addition to
   the cookie option.

0.10.11
-------

-  Fix Delete when not passing a deadline argument.
-  Improve interactive script by importing Transfer and Delete.
-  Add ``interpret_globs`` option to Delete.
-  Fix ``set_submit_type`` in ``ActivationRequirementList`` to properly
   update the mapping.

0.10.10
-------

-  Include CAs in the package; the ``server_ca_file`` parameter (and the
   -C command line arg) is no longer required.
-  Alternate ``delegate_proxy`` activation implementation using a custom
   C program called ``mkproxy`` instead of M2Crypto. See
   ``mkproxy/README.markdown`` for details. ``mkproxy`` is the preferred
   implementations, so if both the executable and M2Crypto are
   installed, ``mkproxy`` is used.
-  Moved examples to package data, so they are included in the PyPI
   package.

0.10.9
------

-  Add https proxy support, using the ``HTTPS_PROXY`` environment
   variable. This has been tested in 2.6.6 and 2.7, and does not work in
   2.6.1 (because the tunnel features was added in the middle of the
   2.6.X cycle). Other versions > 2.6.1 may also work, but this has not
   been tested. Thanks to Brett Viren for this feature!
-  If you have both your key and certificate in the same file, you don't
   have to pass it to both -c and -k when running the examples and
   interactive client. Just pass one of them, and it will assume the
   file contains both.
-  Added some basic usage docs to
   ``examples/delegate_proxy_activate.py``
-  Fix example.py breakage when printing GC endpoints.
-  Import readline in main.py, for more convenient interactive testing.

