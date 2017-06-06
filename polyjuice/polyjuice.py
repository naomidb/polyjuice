#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
docstr = """
Polyjuice

Usage:
    polyjuice.py (-h | --help)
    polyjuice.py [-l | --log] (<input_path> <output_path>) [-z <zip_output_path>]
    polyjuice.py [-l | --log] [-z <zip_output_path>]

Options:
  -h --help                                     Show this message and exit
  -z --zip                                      Archives the output folder
  -l --log                                      Give progress of program

Instructions:
    Run polyjuice on the ISO file or on the Extracted DICOM folder. This will give an ouput folder
containing dicom files with unneccessary tags removed

$ ./polyjuice.py path_to_ISOfile.iso path_to_OutputFolder

Inorder to ZIP your Cleaned Output Directory
$ ./polyjuice.py -z path_to_ISOfile.iso path_to_OutputFolder Path_to_Zipped_file

"""
import os
import os.path
import shutil
import yaml
from docopt import docopt
from filch import DicomCaretaker

INPUT_DIR = '<input_path>'
OUTPUT_DIR = '<output_path>'
ZIP_DIR = '<zip_output_path>'
_print_log = '--log'

def consult_book(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

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

def brew_potion(dicom_file, in_dir, out_dir, deletions, modifications, verbose):
    for path, subdirs, files in os.walk(in_dir):
        for name in files:
            print os.path.join(path, name)
            try:
                with open(os.path.join(path, name)) as working_file:
                    if verbose:
                        print("Working on {}".format(name))
                    dataset = dicom_file.scrub(working_file, deletions, modifications, verbose)
                    dicom_file.save_output(dataset, out_dir, name)
            except Exception, e:
                print("{} failed".format(name))
                print (str(e))

def main(args):
    dicom_dir = args[INPUT_DIR]
    out_dir = args[OUTPUT_DIR]
    consult_book(out_dir)

    dicom_file = DicomCaretaker()

    in_dir = dicom_file.start(dicom_dir)

    config = raid_snapes_cupboard()
    deletions = config.get('deletions')
    modifications = config.get('modifications')

    brew_potion(dicom_file, in_dir, out_dir, deletions, modifications, args[_print_log])

    # Working on converting into ZIP folder
    if(args.get(ZIP_DIR)):
        shutil.make_archive(out_dir, 'zip', out_dir)

    # Checking if the file is ISO    
    dicom_file.end()

# Integrating Things with Docopt
if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
