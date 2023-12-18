if __name__ == '__main__':

    slot = 0

    with open('/flash/program{:02}/program.mpy'.format(slot), 'rb') as file:

        next(file)  # Skip the line with file information.

        for line in file:
            # Try to convert the line in 'utf-8' format and print it.
            try:
                print(str(line.rstrip(), 'utf-8'))
            # If line can't be decoded - skip this line.
            except UnicodeError:
                continue
