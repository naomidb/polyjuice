#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
docstr = """
Polyjuice

Usage: polyjuice.py [-hz] (<input_path> <output_path>) [-z <zip_output_path>]

Options:
  -h --help                                     show this message and exit
  -z --zip                                      Archives the output folder
Instructions:
    Run polyjuice on the ISO file or on the Extracted DICOM folder. This will give an ouput folder
containing dicom files with unneccessary tags removed

$ ./polyjuice.py path_to_ISOfile.iso path_to_OutputFolder

Inorder to ZIP your Cleaned Output Directory
$ ./polyjuice.py -z path_to_ISOfile.iso path_to_OutputFolder Path_to_Zipped_file
"""
import os
import os.path
import dicom
import shutil
from dicom.errors import InvalidDicomError
import yaml
from docopt import docopt

input_dir = '<input_path>'
output_dir = '<output_path>'
zip_output_dir = '<zip_output_path>'
def raid_snapes_cupboard():
    #find what needs to be modified or deleted from config file
    #config_path = args.get('config.yaml', None)
    config_path = 'config.yaml'
    if config_path:
        with open(config_path, 'r') as config_file:
            try:
                config = yaml.load(config_file.read())
            except yaml.YAMLError as exc:
                print(exc)
        return (config)

def deletion(deletion_pointer, delete_me):
    #use list from config file
    for key in delete_me:
        if (key in deletion_pointer):
            ingredient = deletion_pointer.data_element(key).tag
            del deletion_pointer[ingredient]
            print ("{} deleted".format(key))

def modification(modification_pointer, modify_me):
    #use dictionary from config file
    for key in modify_me:
        if (key in modification_pointer):
            ingredient = modification_pointer.data_element(key)
            ingredient.value = modify_me[key]
            print ("{} changed".format(key))

def brew(dataset, out, filename):
    output = os.path.join(out, filename)
    dataset.save_as(output)

def main(args):
    import sys
    if not (args.get(input_dir) and args.get(output_dir)):
        print("Please Enter Input and Output files ")
        sys.exit()
    # dicom_dir, out_dir = sys.argv[1:]
    dicom_dir = args[input_dir]
    out_dir = args[output_dir]
    flag = False
    if(dicom_dir.endswith(".iso")):
        # Work with ISO Stuff
        flag =  True
        # If user gives ISO then pulling DICOM folder from ISO
        os.system("hdiutil mount %s" % dicom_dir)
        in_dir = "/Volumes/DCS/DICOM"
    else:
        in_dir = os.path.join(dicom_dir, "DICOM")
    config = raid_snapes_cupboard()
    delete_me = config.get('deletions')
    modify_me = config.get('modifications')

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for path, subdirs, files in os.walk(in_dir):
        for name in files:
            print os.path.join(path, name)
            try:
                with open(os.path.join(path, name)) as working_file:
                    dicom_pointer = dicom.read_file(working_file)
                    print("Working on {}".format(name))
                    deletion(dicom_pointer, delete_me)
                    modification(dicom_pointer, modify_me)
                    brew(dicom_pointer, out_dir, name)
            except Exception, e:
                print("{} failed".format(name))
                print (str(e))
    # Working on converting into ZIP folder
    if(args.get(zip_output_dir)):
        shutil.make_archive(out_dir, 'zip', out_dir)

    # Checking if the file is ISO
    if flag == True:
        os.system("hdiutil unmount  /Volumes/DCS")

# Integrating Things with Docopt
if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
