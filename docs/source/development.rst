Development
===========

In order to make changes to this library, you will need:

* Python >= 3.12
* Poetry

Poetry Installation
*******************

Install **Poetry** using one of options.

Pip:

.. code-block:: bash

    pip install poetry

Brew:

.. code-block:: bash

    brew install poetry

ASDF:

.. code-block:: bash

    asdf plugin add poetry
    asdf install poetry latest
    asdf global poetry latest


Initialize Project
******************

Use this command to initialize project (along with it's virtualenv) and fetch dependencies.

.. code-block:: bash

    poetry install

In order to run any command inside virtualenv:

.. code-block:: bash

    poetry run command args
    # For example
    poetry run pytest


You may also activate virtualenv inside current terminal (equivalent to source venv) and run commands:

.. code-block:: bash

    poetry shell
    # venv activated
    pytest

Building And Publishing
***********************

Register your PyPI token (once):

.. code-block:: bash

    poetry config pypi-token.pypi your-pypi-token

Build project:

.. code-block:: bash

    poetry build

Publish to PyPI manually:

.. code-block:: bash

    poetry publish

Linting and Formatting
**********************

For linting:

.. code-block:: bash

    ruff check

Ruff may automatically fix minor issues. If not, it will show file with the issue.

For formatting:

.. code-block:: bash

    ruff format