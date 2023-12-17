# About
This project provides a solution to store and manage large data files for use with the Spike Prime Hub via its official app. It has been tested with the SPIKE 3 firmware and app.

> [!IMPORTANT]
> Spike Legacy and Mindstorms Robot Inventor:
> This method doesn't work with Spike Legacy Or Mindstorms.
> [Here](https://github.com/GizmoBricks/get_slots_paths) solution for Spike Legacy and Mindstorms.

# An "exploit":

If a project doesn't contain any Syntax Errors, it will be precompiled by the app into a MicroPython `.mpy` file and stored in the Hub.

A MicroPython file is a binary file. More importantly, as it's a precompiled file, its content will differ from the original file.

But: first docstring of the file will be stored as is. This method capitalizes on this “exploit”.

However, if a project contains any Syntax Errors, it wouldn't be stored in the Hub at all.

# Where are projects stored in the Hub:

All projects reside in the `/flash/program/` directory, each having its own directory. These directories are labeled with two digits, acting as the slot number.

The full path to a project file looks like this: `/flash/program/{XX}/program.mpy`.
