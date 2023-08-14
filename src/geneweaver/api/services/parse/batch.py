from typing import List, Tuple
from fastapi import UploadFile

from geneweaver.core.parse import batch
from geneweaver.core.schema.messages import SystemMessage, UserMessage


from geneweaver.api.services.io import read_file_contents


async def process_batch_file(
    # TODO: Add the database session to the function signature.
    # db: Session,
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

    # TODO: Add the genesets to the database
    # results = [
    #     batch_geneset_for_user(db, user_id, geneset)
    #     for geneset in genesets
    # ]

    # TODO: Return the correct values.
    return [10], [], []
