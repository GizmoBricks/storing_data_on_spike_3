# About
This project provides a solution to store and manage large data files for use with the Spike Prime Hub via its official app. It has been tested with the SPIKE 3 firmware and app.

> [!NOTE]
> Limitations:
> 
> The data file size limit is approximately `120 kb`. It is ~120 000 characters per file (~1 500 lines with 80 characters in each line). Less characters in line - more lines.

> [!IMPORTANT]
> 
> This method doesn't work with Spike Legacy or Mindstorms.
> [Here](https://github.com/GizmoBricks/get_slots_paths) solution for Spike Legacy and Mindstorms.

# An "exploit"
If a project contains any Syntax Errors, it wouldn't be stored in the Hub at all.

If a project doesn't contain any Syntax Errors, it will be precompiled by the app into a MicroPython `.mpy` file and stored in the Hub.

A MicroPython file is a binary file. More importantly, as it's a precompiled file, its content will differ from the original file.

But: first docstring of the file will be stored as is. This method capitalizes on this “exploit”.

# Where are projects stored in the Hub

All projects reside in the `/flash/program/` directory, each having its own directory. These directories are labeled with two digits, acting as the slot number.

The full path to a project file looks like this: `/flash/program/{XX}/program.mpy`.
 - `{XX}` - two digit number of the slot. For slots 0-9, `0` added before slot number (`01` for slot #1).

# How to load data file into the Hub

1.	Create a Python Project with Spike 3 app.
2.	Delete any existing data within the project.
3.	Input or paste your data.
4.	Add triple qoutes before and after your data.
5.	Select slot and run the Project.
6.	Wait for the notification `PM: Compiled` in the console.![File uploading](https://github.com/GizmoBricks/storing_data_on_spike_3/assets/127412675/d30268ed-2938-49f4-8581-97d002cc8a06)

> [!NOTE]
> If you choose to press 'Upload', the app will not notify when upload is copleted.	

> [!CAUTION]
> Do not disconect the hub during file uploading to avoid interruptions or data loss.

> [!IMPORTANT]
> During the file uploading process, the hub might not run any programs.

> [!NOTE]
> Larger data files might take some time to upload.
> For instance, a [file containing 100 000 digits of pi](/examples/slot_3) took approximately 1 minutes to store.

# How to read data from the file

Now you can read data from the slot with [this code](/examples/file_content_reading.py).
This code ignore all raw bynary data and read the data which is stored in the docstring:
``` python
if __name__ == '__main__':

    slot = 0

    with open('/flash/program/{:02}/program.mpy'.format(slot), 'rb') as file:

        next(file)  # Skip the line with file information.

        for line in file:
            # Try to convert the line into 'utf-8' format and print it.
            try:
                print(str(line.rstrip(), 'utf-8'))
            # If line can't be decoded - skip this line.
            except UnicodeError:
                continue
```
Output:

```
9:37:37 PM: Compiled
-------------
Slot 0
ABDEFGHIJKLMNOPQRSTUVWXYZ
```

# Functions

As you can see, the code above is pretty simple. But it may be difficult to read and maintein if code will have many lines inside `try` statement.

So I created two functions to solve this problem.

## The `slot_path` function

[This function](/slot_path.py) constructs absolute path to 'program.mpy' for given `slot`.

### Argument

  - `slot` (`int`, optional): the slot number for which the path is generated [0-19] (default 0).

### Returns
  - `str`: absolute path to 'program.mpy' for given `slot`.

### Raises

  - `ValueError` if `slot` is not in range [0-19].
  - `RuntimeError` if given `slot` is empty.

## The `mpy_to_text` function

[This function](/mpy_to_text.py) converts a line of a '.mpy' file to a UTF-8 string. If the line contains raw binary data, it returns an empty string. To use, skip the first line of the file using 'next()' before calling this function.

### Argument

  - `line` (`bytes`): a line of a '.mpy' file in binary format.

### Returns
  - `str`: a UTF-8 string decoded from the input line, or an empty string if the line contains raw binary data that cannot be decoded.

## Examples
### File reading
This [code](/examples/onother_way_to_read_file_content.py) demonstrates how to retrieve the file path associated with the slot number `0` and print the contents of the file. 
``` python
def slot_path(slot: int = 0) -> str:
   # Rest of the slot_path implementation...
    return path


def mpy_to_text(line: bytes) -> str:
    # Rest of the mpy_to_text implementation...
    return output


if __name__ == '__main__':
    slot = 0
    with open(slot_path(slot), 'rb') as file:
        next(file)  # Skip the line with file information.
        for line in file:
            print(mpy_to_text(line).rstrip())
```

Output:

```
7:08:44 PM: Compiled
-------------
Slot 0
ABDEFGHIJKLMNOPQRSTUVWXYZ
```

To run this example:
* Upload [this file](/examples/onother_way_to_read_file_content.py) into slot #19.
* Upload [this data](/examples/slot_0) into slot #0 and run program from slot #19.

### Count occurances in a large file
This [code](/examples/occurrences_counting.py) demonstrates how to retrieve the file paths associated with the slots `3`-`12`, count and print the occurrences of each digit (0-9) within data files from the slots [3-12].

``` python
def slot_path(slot: int = 0) -> str:
   # Rest of the slot_path implementation...
    return path


def mpy_to_text(line: bytes) -> str:
    # Rest of the mpy_to_text implementation...
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
```

Output:
```
6:56:49 PM: Compiled
-------------
Currently processing: slot #3...
Currently processing: slot #4...
Currently processing: slot #5...
Currently processing: slot #6...
Currently processing: slot #7...
Currently processing: slot #8...
Currently processing: slot #9...
Currently processing: slot #10...
Currently processing: slot #11...
Currently processing: slot #12...
0 occurs 99959 times.
1 occurs 99758 times.
2 occurs 100026 times.
3 occurs 100229 times.
4 occurs 100230 times.
5 occurs 100359 times.
6 occurs 99548 times.
7 occurs 99800 times.
8 occurs 99985 times.
9 occurs 100106 times.
Total: 1000000
```

To run this example:
* Upload [this file](/examples/occurrences_counting.py) into slot #19.
* Upload [this data](/examples/slot_3) into slot #3.
* Upload [this data](/examples/slot_4) into slot #4.
* Upload [this data](/examples/slot_5) into slot #5.
* Upload [this data](/examples/slot_6) into slot #6.
* Upload [this data](/examples/slot_7) into slot #7.
* Upload [this data](/examples/slot_8) into slot #8.
* Upload [this data](/examples/slot_9) into slot #9.
* Upload [this data](/examples/slot_10) into slot #10.
* Upload [this data](/examples/slot_11) into slot #11.
* Upload [this data](/examples/slot_12) into slot #12.
* Run program from slot #19.
> [!NOTE]
> It may take some time to store each data file and 2 and a half minutes to compete program.
