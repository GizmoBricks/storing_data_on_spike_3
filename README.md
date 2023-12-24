# About
This project provides a solution to store and manage large data files 
for use with the Spike Prime Hub via its official app. 
It has been tested with the Spike 3 firmware and app.

> [!NOTE]
> Limitations:
> 
> The data file size limit is approximately `120 kb`, 
> equivalent to ~120 000 characters per file 
> (~1 500 lines with 80 characters per line). 
> Fewer characters per line allows for more lines.

> [!IMPORTANT]
> 
> This method doesn't work with Spike Legacy or Mindstorms.
> [Here](https://github.com/GizmoBricks/get_slots_paths) solution 
> for Spike Legacy and Mindstorms.

> [!IMPORTANT]
>
> Known Issue:
> 
> When the Hub is connected via Bluetooth and the code running 
> on the Hub prints a substantial amount of data in the app console 
> (several hundred lines), there is a possibility of data loss. 
> This issue specifically pertains to the print() function.
>
> This problem does not affect the Hub's ability to work with data; 
> it can still manage large data sets without any issues. 
> However, the concern arises solely when using the print() function 
> in a large loop under Bluetooth connectivity.
>
> Fortunately, when the Hub is connected via USB, 
> all functions work correctly without any data loss or interruptions.

# An "exploit"

If a project contains Syntax Errors, it won't be stored in the Hub. 
Conversely, a Syntax-Error-free project will be precompiled 
into a MicroPython `.mpy` file by the app and stored in the Hub. 
However, the precompiled file content differs from the original.

The initial docstring of the file remains intact, 
which serves as the basis for this "exploit."

# Project Storage in the Hub

Projects reside in the `/flash/program/` directory, 
each having a designated directory labeled with two digits, 
representing the slot number. The full path to a project file 
appears as `/flash/program/{XX}/program.mpy`, 
where `{XX}` denotes the two-digit slot number 
(with a leading `0` for slots #1-9).

# Uploading Data Files to the Hub

Follow these steps to load a data file into the Hub using the Spike 3 app:

1.	Create a Python Project within Spike 3 app.
2.	Delete any existing data within the project.
3.	Input or paste your data.
4.	Enclose your data with triple quotes.
5.	Select slot and run the Project.
> [!NOTE]
> Selecting 'Upload' won't provide a notification upon completion.	   
6.	Wait for the notification `Compiled` in the console.
    ![File uploading](https://github.com/GizmoBricks/storing_data_on_spike_3/assets/127412675/d30268ed-2938-49f4-8581-97d002cc8a06)

> [!CAUTION]
> Do not disconnect the hub during file uploading to avoid interruptions 
> or data loss.

> [!IMPORTANT]
> During the file uploading process, the hub may not run any programs.

> [!NOTE]
> Larger data files may require more time to upload.
> For example, a [file containing 100 000 digits of pi](/examples/slot_3) 
> took approximately 1 minutes to store.

# Reading Data from the File

The code below demonstrate how to read data from the slot #0.
This code ignore all raw binary data and reads the content stored 
in the docstring.
```python
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
```
Output:

```
9:37:37 PM: Compiled
-------------
Slot 0
ABDEFGHIJKLMNOPQRSTUVWXYZ
```

To run this example:
* Upload [this data](/examples/slot_0) into slot #0.
* Upload [this code](/examples/file_content_reading.py) into slot #19.
* Run program from slot #19.

# The `get_data_paths` function

[This function](/get_data_paths.py) 

This function retrieves the paths associated with available slots
with files which contain initial docstring. 
Function ignores slots with files which does not contain initial docstring.

### Arguments

- do_check (bool, optional): Flag to indicate whether to perform
  a file format check (default: False).
- check_word (str, optional): The word used for file format checking
  (default: empty string).  

### Returns
  
- dict: The dictionary of available slots and their paths, 
  or empty dictionary, if no available slots.
> [!NOTE]
> The dictionary is not sorted.

### What the function exactly does

This get_data_path function is designed to scan through a directory structure 
that contains files named `program.mpy` in various slots (from 0 to 19).
It tries to open and read these files. In case an `OSError` or `UnicodeError` 
it continues the next iteration, skipping the current slot.

Then it reads the first line of the file, and if the line does not contain
the bytes object b'__doc__', it continues to the next slot.

Then the function applies optional file format check:
* If do_check is set to True, it performs an additional check 
  based on the check_word.
* It reads first word of the line and compares it with check_word.
* If the condition fails
  (i.e., the first word of the line is not equal to check_word), 
  it continues to the next slot.

If all conditions pass, it stores the slot number as the key 
in the paths_dict dictionary and associates it with the path (file path) 
as the corresponding value.

## Examples
### File reading
This code demonstrates retrieving the file path associated 
with slot number `0` and printing the file content. 

```python
def get_data_paths(do_check: bool = False, check_word: str = '') -> dict:
    # Rest of the function implementation...
    return paths_dict


if __name__ == '__main__':
    slot = 1
    paths = get_data_paths()
    
    if slot in paths:
        with open(paths[slot], 'rb') as file:
            next(file)
            for line in file:
                try:
                    print(str(line, 'utf-8').rstrip())
                except UnicodeError:
                    break
    else:
        print('Slot {} is empty or file does not contain initial docstring.'
              ''.format(slot))
```

Output:

```
7:08:44 PM: Compiled
-------------
Slot 0
ABDEFGHIJKLMNOPQRSTUVWXYZ
```

To run this example:
* Upload [this data](/examples/slot_0) into slot #0.
* Upload [this code](/examples/another_way_to_read_file_content.py) into slot #19.
* Run program from slot #19.

### Count occurrences in a large file
This code calculates and prints the occurrences of each digit (0-9) 
within data files from slots `3` to `12`.

```python
def get_data_paths(do_check: bool = False, check_word: str = '') -> dict:
    # Rest of the function implementation...
    return paths_dict


if __name__ == '__main__':

    first_slot = 3
    num_of_slots = 10

    paths = get_data_paths()
    number_of_occurrences = [0 for _ in range(10)]

    for slot in range(first_slot, first_slot + num_of_slots):

        if slot in paths:

            with open(paths[slot], 'rb') as file:

                print('Currently processing: slot #{}...'.format(slot))
                next(file)  # Skip the line with file information.

                # Skip line to avoid counting '3' before
                # the decimal point:
                if slot == first_slot:
                    next(file)

                for line in file:
                    try:
                        for i in range(10):
                            number_of_occurrences[i] += str(
                                line, 'utf-8').count(str(i))
                    except UnicodeError:
                        break
        else:
            print("Slot {} is empty or doesn't contain initial docstring. "
                  "It will be skipped when counting occurrences.")

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
* Upload [this code](/examples/occurrences_counting.py) into slot #19.
* Run program from slot #19.
  
> [!NOTE]
> Uploading and running the program may take considerable time, especially when handling multiple data files.
