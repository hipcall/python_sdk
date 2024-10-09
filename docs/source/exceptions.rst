Exceptions
==========

There are several exceptions defined for `hipcall-sdk`.

BadRequestException
*******************
Raised for invalid requests. Check your query parameters.

NotFoundException
*****************
Raised for non-existing records.

UnauthorizedException
*********************
Raised for authentication errors. Check your API token and base URL.

UnprocessableEntityException
****************************
Raised for content creation errors. Check your Pydantic data model used for POST requests.

HipcallAPIException
*******************
Raised for any other errors. You may open an issue at `Github repository <https://github.com/hipcall/python_sdk>`_.