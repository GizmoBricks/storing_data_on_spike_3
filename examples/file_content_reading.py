if __name__ == '__main__':

    slot = 0

    with open('/flash/program/{:02}/program.mpy'.format(slot), 'rb') as file:

        # Skip the line with file information.
        next(file)

        for line in file:
            # Try to convert the line into 'utf-8' format and print it.
            try:
                print(str(line.rstrip(), 'utf-8'))
            # If line can't be decoded - stop iterating over the file:
            except UnicodeError:
                break
