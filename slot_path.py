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
