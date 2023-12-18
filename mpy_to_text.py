def mpy_to_text(line: bytes) -> str:
    """
    Converts a line of a '.mpy' file to a UTF-8 string.
    If the line contains raw binary data, it returns an empty string.
    To use, skip the first line of the file using 'next()'
    before calling this function.

    Args:
    - line (bytes): A line of a '.mpy' file in binary format.

    Returns:
    - str: A UTF-8 string decoded from the input line, or an empty string
        if the line contains raw binary data that cannot be decoded.
    """
    try:
        output = str(line, 'utf_8', 'ignore')
    except UnicodeError:
        output = ''
    return output
