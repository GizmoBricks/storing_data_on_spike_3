def get_data_paths(do_check: bool = False, check_word: str = '') -> dict:
    """
    This function retrieves the paths associated with available slots
    with files which contain initial docstring.
    Function ignores slots with files which does not contain 
    initial docstring.

    Args:
    - do_check (bool, optional): Flag to indicate whether to perform
                                a file format check (default: False).
    - check_word (str, optional): The word used for file format checking
                                (default: empty string).

    Returns:
    - dict: The dictionary of available slots and their paths,
            or empty dictionary, if no available slots.

    File format check:
    If the do_check argument is True, the function compares
    the first word of the initial docstring with check_word.
    If they match, the test is passed.
    If they are different, that slot-path pair won't be included
    into the dictionary.

    Note: this function does not work with SPIKE Legacy or
    Mindstorms Robot Inventor.
    """
    paths_dict = {}
    for slot in range(20):
        path = '/flash/program/{:02}/program.mpy'.format(slot)
        
        try:
            with open(path, 'rb') as test_file:
                if b'__doc__' not in test_file.readline():
                    continue

                line = str(test_file.readline(), 'utf-8')

        except (OSError, UnicodeError) as _:
            continue
        
        if do_check and line.split()[0] != check_word:
            continue

        paths_dict[slot] = path
    
    return paths_dict
