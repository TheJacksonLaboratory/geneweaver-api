"""Services for reading and writing files."""

from fastapi import UploadFile


async def read_file_contents(batch_file: UploadFile, encoding: str = "utf-8") -> str:
    """Read the contents of an async file and decodes it using a specified encoding.

    This function uses an asynchronous read operation to get the contents of the
    batch_file, and then decodes those contents from bytes to a string using the
    provided encoding. The default encoding is UTF-8.

    :param batch_file: An instance of UploadFile representing the file to be read.
    :param encoding: The character encoding to use when decoding the file contents.
    Default is 'utf-8'.

    :returns: The contents of the file as a string decoded using the specified encoding.
    """
    contents = await batch_file.read()
    return contents.decode(encoding)
