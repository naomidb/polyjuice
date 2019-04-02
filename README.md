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

If a file does not have the 'DICM' marker, it will fail. If a file you need to read is failing, you can add `force=True` on `read_file` (in dicom_image).

`self._dataset = dicom.read_file(dicom_file, force=True)`

## Polyjuice walk-through

*go_to_library()*: Retrieve the config file

*ask_hermione()*: Check if the given directory exists. If it does not, create it.

*browse_restricted_section()*: Walk through input directory and send individual files to brew_potion(). If the file is an iso, mount it and call itself to walk through the mounted image.

*brew_potion()*: Send the dicom image files to be cleaned and otherwise modified. Find appropriate folder names.

*add_hair()*: Archive the folders created.

## Making use of the config file

The config file contains several ways to help you customize your project.

The first key, zip, allows you to choose the location your archived files will be sent to.

The second key, new_IDs, allows you to provide a link to a csv file to update the patient Ids. The csv file should have the old IDs in the first column and the new IDs in the second column.

The next key, modifications, has all the tags that will undergo some change. The tag to be modified should have its name as the key and the desired change should be the value. To delete a tag, the value should be `Null`.

The modifications listed in the config file were selected in accordance with the [DICOM Standards Committee](ftp://medical.nema.org/medical/dicom/final/sup55_ft.pdf). You can add and remove, comment and uncomment as desired for your project.

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
