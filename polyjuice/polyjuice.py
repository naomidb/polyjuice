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

def browse_restricted_section(parent_file, out_dir, zip_dir, modifications, verbose):
    for current_file in os.listdir(parent_file):
        print("Current File: " + current_file)
        dicom_dir = os.path.join(parent_file, current_file)
        consult_book(dicom_dir, out_dir, zip_dir, modifications, verbose)

def consult_book(dicom_dir, out_dir, zip_dir, modifications, verbose):
    editor = DicomCaretaker()
    editor.get_progress()
    in_dir = editor.start(dicom_dir, out_dir)

    brew_potion(editor, in_dir, out_dir, modifications, zip_dir, verbose)

    # Checking if the file is ISO
    editor.end()

def brew_potion(editor, in_dir, out_dir, modifications, zip_dir, verbose):
    new_dicom = False
    dicom_folders = []
    for path, subdirs, files in os.walk(in_dir):
        for name in files:
            log_path = os.path.join(out_dir, 'log.txt')
            if verbose:
                log = Lumberjack(log_path, True)
            else:
                log = Lumberjack(log_path)
            path_message = os.path.join(path, name)
            log(path_message)
            try:
                with open(os.path.join(path, name)) as working_file:
                    working_message = "Working on {}".format(name)
                    log(working_message)

                    dataset = DicomImage(working_file)

                    editor.scrub(dataset, modifications, log)

                    folder_name = editor.get_folder_name(dataset)
                    identified_folder = os.path.join(out_dir, folder_name)

                    if not os.path.exists(identified_folder):
                        ask_hermione(identified_folder)
                        dicom_folders.append(identified_folder)

                    editor.save_output(dataset, identified_folder, name)
                    saving_message = "Saved to {}".format(identified_folder)
                    log(saving_message)

                    new_dicom = True

            except Exception, e:
                print("{} failed".format(name))
                print (str(e))
                failure_message = "{} failed".format(name) + "\n" + str(e)
                log(failure_message)

    if zip_dir and new_dicom:
        add_hair(dicom_folders, zip_dir, log)


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
    if args[CONFIG_PATH]:
        config_path = args[CONFIG_PATH]
    else:
        config_path = 'config.yaml'

    config = go_to_library(config_path)
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
            if args[_has_multiple]:
                #Loop through ISOs and subdirectories
                parent_file = os.path.join(in_root, io_pair['input'])
                browse_restricted_section(parent_file, out_dir, zip_dir, modifications, verbose)
            else:
                dicom_dir = os.path.join(in_root, io_pair['input'])
                consult_book(dicom_dir, out_dir, zip_dir, modifications, verbose)

    elif args[_has_multiple]:
        #Loop through ISOs and subdirectories
        parent_file = args[INPUT_DIR]
        out_dir = args[OUTPUT_DIR]
        ask_hermione(out_dir)
        browse_restricted_section(parent_file, out_dir, zip_dir, modifications, verbose)

    else:
        dicom_dir = args[INPUT_DIR]
        out_dir = args[OUTPUT_DIR]
        ask_hermione(out_dir)
        consult_book(dicom_dir, out_dir, zip_dir, modifications, verbose)


# Integrating Things with Docopt
if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
