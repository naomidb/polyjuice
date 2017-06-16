#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
docstr = """
Polyjuice
Usage:
    polyjuice.py (-h | --help)
    polyjuice.py [-lzm]  (<input_path> <output_path>) [<config_file>]
    polyjuice.py [-lzcm] [<config_file>]
Options:
  -h --help                     Show this message and exit
  -z --zip                      Archives the output folder
  -l --log                      Give progress of program
  -c --config                   Use config file to get input and output paths
  -m --multiple                 Use input folder with multiple ISOs or directories that should have unique output folders
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
import time
#import progressbar
from docopt import docopt
from lumberjack import Lumberjack
from filch import DicomCaretaker
from dicom_image import DicomImage

CONFIG_PATH = '<config_file>'
INPUT_DIR = '<input_path>'
OUTPUT_DIR = '<output_path>'
_print_log = '--log'
_zip_folder = '--zip'
_use_config = '--config'
_has_multiple = '--multiple'
dicom_folders = []

def go_to_library(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except:
        print("Error: Check config file")
        exit()
    return config

def ask_hermione(out_dir):
    if not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
        except Exception as e:
            raise e

def browse_restricted_section(parent_file, out_dir, zip_dir, modifications, log):
    #find files and return list
    editor = DicomCaretaker()

    for path, subdirs, files in os.walk(parent_file):
        for name in files:
            path_message = os.path.join(path, name)
            log(path_message)
            try:
                check_file_type = os.path.join(path, name)
                working_file = os.path.join(path, name)
                if check_file_type.endswith(".iso"):
                    # Do Mounting and Unmounting Stuff
                    new_parent_dir = editor.mount_iso(working_file, out_dir)
                    browse_restricted_section(new_parent_dir,out_dir,zip_dir,modifications,verbose)
                    editor.end()
                    # new_dicom  = brew_potion(editor, working_file, out_dir, modifications, log,name)

                else:
                    # Do Normal Cleaning Stuff
                    brew_potion(editor, working_file, out_dir, modifications, log,name)

            except Exception, e:
                print("{} failed".format(name))
                print (str(e))
                failure_message = "{} failed".format(name) + "\n" + str(e)
                log(failure_message)


# def consult_book(dicom_dir, out_dir, zip_dir, modifications, verbose):
#     editor = DicomCaretaker()
#     in_dir = editor.mount_iso(dicom_dir, out_dir)
#
#     brew_potion(editor, in_dir, out_dir, modifications, zip_dir, verbose)
#
#     # Checking if the file is ISO
#     editor.end()

def brew_potion(editor, working_file, out_dir, modifications,log,name):
    try:
        with open(working_file) as working_file:
            working_message = "Working on {}".format(name)
            log(working_message)
            # print working_message
            image = DicomImage(working_file)

            editor.scrub(image, modifications, log)

            folder_name = editor.get_folder_name(image)
            identified_folder = os.path.join(out_dir, folder_name)

            if not os.path.exists(identified_folder):
                ask_hermione(identified_folder)
                dicom_folders.append(identified_folder)

            editor.save_output(image, identified_folder, name)
            saving_message = "Saved to {}".format(identified_folder)
            log(saving_message)

    except Exception, e:
        print("{} failed".format(name))
        print (str(e))
        failure_message = "{} failed".format(name) + "\n" + str(e)
        log(failure_message)

def add_hair(dicom_folders, zip_dir, log):
    for folder in dicom_folders:
        shutil.make_archive(folder, 'zip', folder)
        zipped_message = "{} archived".format(folder)
        log(zipped_message)

        ask_hermione(zip_dir)
        os.system("mv {}.zip {}".format(folder, zip_dir))
        move_zip_message = "{} moved to {}".format(folder, zip_dir)
        log(move_zip_message)

def main(args):
    if not args[CONFIG_PATH]:
        args[CONFIG_PATH] = 'config.yaml'

    config = go_to_library(args[CONFIG_PATH])
    modifications = config.get('modifications')

    if args[_zip_folder]:
        zip_dir = config.get('zip')
        print("zip folder " + str(zip_dir))
    else:
        zip_dir = None

    verbose = args[_print_log]

    if args[_use_config]:
        #get from config file
        in_root = config.get('in_data_root')
        out_root = config.get('out_data_root')
        io_pairs = config.get('io_pairs')

        for io_pair in io_pairs:
            out_dir = os.path.join(out_root, io_pair['output'])
            ask_hermione(out_dir)
            log_path = os.path.join(out_dir, 'log.txt')
            log = Lumberjack(log_path, verbose)
            parent_file = os.path.join(in_root, io_pair['input'])
            browse_restricted_section(parent_file, out_dir, zip_dir, modifications, log)

    else:
        #Loop through ISOs and subdirectories
        parent_file = args[INPUT_DIR]
        out_dir = args[OUTPUT_DIR]
        ask_hermione(out_dir)
        log_path = os.path.join(out_dir, 'log.txt')
        log = Lumberjack(log_path, verbose)
        browse_restricted_section(parent_file, out_dir, zip_dir, modifications, log)
        
    if zip_dir:
        add_hair(dicom_folders, zip_dir, log)

    # else:
    #     dicom_dir = args[INPUT_DIR]
    #     out_dir = args[OUTPUT_DIR]
    #     ask_hermione(out_dir)
    #     consult_book(dicom_dir, out_dir, zip_dir, modifications, verbose)

        #TODO: Find where to put progress bar
        '''bar = progressbar.ProgressBar()
        for i in bar(range(100)):
            time.sleep(2)'''

# Integrating Things with Docopt
if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
