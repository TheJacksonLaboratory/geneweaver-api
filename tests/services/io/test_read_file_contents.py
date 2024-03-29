""""Unit tests for the read_file_contents function in the io module."""

import pytest
from geneweaver.api.services import io


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    ("contents", "encoding", "expected"),
    [
        # normal UTF-8 encoded text
        (b"Hello, world!", "utf-8", "Hello, world!"),
        # improperly encoded UTF-8 text
        (b"\x80abc", "utf-8", UnicodeDecodeError),
        # ASCII encoded text
        (b"Hello, world!", "ascii", "Hello, world!"),
        # Empty file
        (b"", "utf-8", ""),
        # Non-English characters (Japanese, in this case)
        (
            b"\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3"
            b"\x81\xaf\xe3\x80\x81\xe4\xb8\x96\xe7\x95\x8c!",
            "utf-8",
            "こんにちは、世界!",
        ),
        # Non-English characters (Arabic, in this case)
        (
            b"\xd9\x85\xd8\xb1\xd8\xad\xd8\xa8\xd8\xa7\xd8\x8c "
            b"\xd8\xa7\xd9\x84\xd8\xb9\xd8\xa7\xd9\x84\xd9\x85!",
            "utf-8",
            "مرحبا، العالم!",
        ),
        # Non-English characters (Greek, in this case)
        (
            b"\xce\x93\xce\xb5\xce\xb9\xce\xac \xcf\x83\xce\xbf\xcf\x85, "
            b"\xce\xba\xcf\x8c\xcf\x83\xce\xbc\xce\xbf!",
            "utf-8",
            "Γειά σου, κόσμο!",
        ),
        # Non-English characters (Hindi, in this case)
        (
            b"\xe0\xa4\xa8\xe0\xa4\xae\xe0\xa4\xb8"
            b"\xe0\xa5\x8d\xe0\xa4\xa4\xe0\xa5\x87, "
            b"\xe0\xa4\xa6\xe0\xa5\x81\xe0\xa4\xa8"
            b"\xe0\xa4\xbf\xe0\xa4\xaf\xe0\xa4\xbe!",
            "utf-8",
            "नमस्ते, दुनिया!",
        ),
        # Non-English characters (Hebrew, in this case)
        (
            b"\xd7\xa9\xd7\x9c\xd7\x95\xd7\x9d, \xd7\xa2\xd7\x95\xd7\x9c\xd7\x9d!",
            "utf-8",
            "שלום, עולם!",
        ),
        # Unicode characters
        (b"\xe2\x9c\x88 World!", "utf-8", "✈ World!"),
        # Different encoding (ISO-8859-1)
        (b"Hello, world!", "ISO-8859-1", "Hello, world!"),
        # Improperly encoded text
        (b"\x80\xe2\x82\xac", "utf-8", UnicodeDecodeError),
        # Attempt to decode byte sequence not valid in UTF-8
        (b"Hello, world!", "unknown_encoding", LookupError),
        # Use of an unknown encoding
        (b"\x80abc", "ascii", UnicodeDecodeError),
        # Attempt to decode byte sequence not valid in ASCII
        (
            b"\xd9\x85\xd8\xb1\xd8\xad\xd8\xa8\xd8\xa7\xd8\x8c "
            b"\xd8\xa7\xd9\x84\xd8\xb9\xd8\xa7\xd9\x84\xd9\x85!",
            "ascii",
            UnicodeDecodeError,
        ),
        # Attempt to decode non-ASCII byte sequence with ASCII encoding
    ],
)
async def test_read_file_contents(contents, encoding, expected, mock_upload_file):
    """Test the read_file_contents function."""
    # Set up the mock to return the test contents when read
    mock_upload_file.read.return_value = contents

    if expected is UnicodeDecodeError or expected is LookupError:
        # If the test case expects a UnicodeDecodeError, check if it raises
        with pytest.raises(expected):
            await io.read_file_contents(mock_upload_file, encoding)
    else:
        # Otherwise, just assert the expected and actual outputs match
        assert await io.read_file_contents(mock_upload_file, encoding) == expected

    assert mock_upload_file.read.called
