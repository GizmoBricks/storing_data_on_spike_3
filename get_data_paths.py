def get_data_paths(do_check: bool = False, check_word: str = '') -> dict:
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
