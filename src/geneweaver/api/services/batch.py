"""Service functions for dealing with batch files."""
from enum import Enum
from typing import List, Tuple

from fastapi import UploadFile

from geneweaver.core.parse import batch

from geneweaver.api.schemas.batch import BatchUploadGeneset, GenesetValueInput
from geneweaver.api.schemas.messages import SystemMessage, UserMessage


async def process_batch_file(
    batch_file: UploadFile,
    user_id: int,
) -> Tuple[List[int], List[UserMessage], List[SystemMessage]]:
    """Asynchronously processes a batch file for geneset information.

    This function reads the contents of a batch file and processes each line to extract
    geneset information. Exceptions encountered during processing are caught and
    returned as UserMessage and SystemMessage instances.

    Note: The function is not complete and currently returns placeholder values.

    :param batch_file: An instance of UploadFile representing the file to be processed.
    :param user_id: The ID of the user performing the operation.

    :returns: A tuple containing placeholder data:
        0. The first element is a list of integers,
        1. the second is a list of UserMessage instances,
        2. and the third is a list of SystemMessage instances.
    """
    contents = await read_file_contents(batch_file)
    genesets = batch.process_lines(contents)

    # TODO: Remove this print statement.
    for geneset in genesets:
        print(geneset, "\n")

    # TODO: Return the correct values.
    return [10], [], []


async def read_file_contents(batch_file: UploadFile, encoding: str = "utf-8") -> str:
    """Reads the contents of an async file and decodes it using a specified encoding.

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
