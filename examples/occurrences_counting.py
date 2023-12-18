def slot_path(slot: int = 0) -> str:
    """
    Constructs absolute path to 'program.mpy' for given slot.

    Args:
    - slot (int, optional): The slot number
                            for which the path is generated [0-19]
                            (default 0).

    Returns:
    - str: absolute path to 'program.mpy' for given slot.

    Raises:
    - ValueError if slot is not in range [0-19].
    - RuntimeError if given slot is empty.
    """
    if not (0 <= slot <= 19):
        raise ValueError('slot argument not in range [0-19].')
    path = '/flash/program/{:02}/program.mpy'.format(slot)
    try:
        with open(path) as _:
            pass
    except OSError:
        raise RuntimeError('Slot {} is empty.'.format(slot))
    return path


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


if __name__ == '__main__':
    first_slot = 3
    last_slot = first_slot + 9

    number_of_occurrences = [0 for _ in range(10)]

    for slot in range(first_slot, last_slot + 1):

        try:
            with open(slot_path(slot), 'rb') as file:
                print('Currently processing: slot #{}...'.format(slot))
                if slot == first_slot:
                    next(file)
                next(file)  # Skip the line with file information.
                for line in file:
                    for i in range(10):
                        number_of_occurrences[i] += mpy_to_text(line).count(
                                                                        str(i))
        except OSError:
            continue

    for i in range(10):
        print('{} occurs {} times.'.format(i, number_of_occurrences[i]))
    print('Total: {}'.format(sum(number_of_occurrences)))
