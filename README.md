polyjuice
======

Polyjuice will anonymize dicom files. What gets modified or deleted can easily be changed by editing the config file.

## Requirements

Polyjuice works on OSX and Linux.

## Using polyjuice

`python polyjuice.py /my/path/to/input/folder /my/path/to/output/folder`

You can view polyjuice usage in the terminal with the `-h` or `--help` flag.

There are two ways to use polyjuice.

1. Write the input and output paths in the terminal

2. Write the input and output paths in the config file.

If you use the second option, you must use the `-c` or `--config` flag. However, this allows you to have multiple input and output folders in one run.

You can also use the `-z` or `--zip` flag to archive the output folders. The desired location of your archived files is written in the config file.

Note that neither the output directory nor the archive directory need exist before running the program. If they do not exist, Polyjuice will make them for you.

If a file does not have the 'DICM' marker, it will fail. If a file you need to read is failing, you can add `force=True` on `read_file` (in filch.py).

`dataset = dicom.read_file(working_file, force=True)`

## Making use of the config file

The config file contains several ways to help you customize your project.

The first key, zip, allows you to choose the location your archived files will be sent to.

The next key contains tags that will be deleted from the DICOM files. The following, modifications, contains tags that will be modified. The dictionary inside modifications has the name in the key position and the desired value for the tag in the value position.

The modifications listed in the config file were selected in accordance with the [DICOM Standards Committee](ftp://medical.nema.org/medical/dicom/final/sup55_ft.pdf). You can add or remove, comment and uncomment as desired for your project.

The next two keys, in_data_root and out_data_root, contain the root for the input and output folders.

Finally, the io_pairs key contains a dictionary with the input and output files. If you use the preceding two keys for the file roots, these **must** not start with a `/` or they will be interpreted as an absolute path and ignore the roots. However, you can use sub-directories in the io_pair dictionary while still using the roots.

```
in_data_root: /my/root/input/path
out_data_root: /my/root/output/path

io_pairs:
    - input: with/sub/directory/my_file.iso
    - output: output_folder
```

References
------

Pydicom: <https://github.com/pydicom/pydicom>

License
------

Apache 2: <http://www.apache.org/licenses/LICENSE-2.0>
