======================
kiwitcms-pytest-plugin
======================

.. image:: https://img.shields.io/pypi/v/kiwitcms-pytest-plugin.svg
    :target: https://pypi.org/project/kiwitcms-pytest-plugin
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/kiwitcms-pytest-plugin.svg
    :target: https://pypi.org/project/kiwitcms-pytest-plugin
    :alt: Python versions

.. image:: https://tidelift.com/badges/package/pypi/kiwitcms
    :target: https://tidelift.com/subscription/pkg/pypi-kiwitcms?utm_source=pypi-kiwitcms&utm_medium=github&utm_campaign=readme
    :alt: Tidelift

.. image:: https://opencollective.com/kiwitcms/tiers/sponsor/badge.svg?label=sponsors&color=brightgreen
   :target: https://opencollective.com/kiwitcms#contributors
   :alt: Become a sponsor

.. image:: https://img.shields.io/twitter/follow/KiwiTCMS.svg
    :target: https://twitter.com/KiwiTCMS
    :alt: Kiwi TCMS on Twitter


This is a `pytest`_ plugin for `Kiwi TCMS <http://kiwitcms.org>`_.


Installation
------------

You can install "kiwitcms-pytest-plugin" via `pip`_ from `PyPI`_::

    $ pip install kiwitcms-pytest-plugin


Configuration and environment
-----------------------------

Minimal config file `~/.tcms.conf`::

    [tcms]
    url = https://tcms.server/xml-rpc/
    username = your-username
    password = your-password


For more info see `tcms-api docs <https://tcms-api.readthedocs.io>`_.
Further documentation and behavior specification can be found
`here <https://tcms-api.readthedocs.io/en/latest/modules/tcms_api.plugin_helpers.html>`_.


Usage
-----

::

    # define environment variables
    pytest -p tcms_pytest_plugin --kiwitcms


Changelog
---------

v12.7 (11 Dec 2023)
~~~~~~~~~~~~~~~~~~~

- Follow versioning of other plugins for Kiwi TCMS
- Update tcms-api from 11.3 to 12.7
- Build and test with Python 3.11
- Add code scanning with CodeQL


v0.1.0 (05 Jul 2022)
~~~~~~~~~~~~~~~~~~~~

- First release on PyPI
- Based on tcms-api v11.3
- Compatible with Kiwi TCMS v11.3 or later


License
-------

Distributed under the terms of the `GNU GPL v3.0`_ license,
"kiwitcms-pytest-plugin" is free and open source software


Authors
-------

- `Dmitry Dygalo <https://github.com/Stranger6667>`_
- `Bryan Mutai <https://github.com/brymut>`_
- `Alex Todorov <https://github.com/atodorov>`_


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.

.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`file an issue`: https://github.com/kiwitcms/pytest-plugin/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
