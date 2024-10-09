Quickstart
==========
hipcall-sdk is a wrapper library built for Hipcall's REST API.

It provides sync and async versions of REST API operations via Python. It also utilizes
Pydantic for data modelling.


Installation
************

You can install this library through pip.

.. code-block:: bash

    $ pip install hipcall-sdk

Usage
*****

After installing the library, just import the client, pass API token and/or base URL.

.. code-block:: python

    >>> from hipcall_sdk.client import Client
    >>> client = Client(api_key="<your-api-key>")
    >>> client.get_calls()

You may also change base URL if necessary. It defaults to `https://use.hipcall.com.tr`

.. code-block:: python

    >>> client = Client(api_key="<your-api-key>", base_url="https://use.hipcall.co.uk")


Async Client
************

Every operation defined in `hipcall_sdk.client.Client` has identical async versions. In order to
use it, import `hipcall.client.AsyncClient`. Example:

.. code-block:: python

    import asyncio
    from hipcall_sdk.client import AsyncClient

    async def main():
        async with AsyncClient(api_key="<your-api-key>") as client:
            calls = await client.get_calls()

    if __name__ == "__main__":
        asyncio.run(main())