polyjuice
======

Polyjuice will anonymize dicom files. What gets modified or deleted can easily be changed by editing the config file.

## Requirements

Polyjuice works on OSX.

## Using polyjuice

To use polyjuice, you will need to type in the name of the program, the path to the input directory, and the path for the output directory (which need not already exist).

`python polyjuice.py /my/path/to/input/folder /my/path/to/output/folder`

To run polyjuice, the dicom images **must** be in a folder named "DICOM" inside the input directory. Beyond the DICOM directory, the file structure does not matter.

If a file is not a dicom file, the program will say that it failed. If you need the program to run on a certain file and it will not, you can add `force=True` on `read_file`.

`dicom_pointer = dicom.read_file(working_file, force=True)`

References
------

Pydicom: <https://github.com/pydicom/pydicom>

License
------

Apache 2: <http://www.apache.org/licenses/LICENSE-2.0>