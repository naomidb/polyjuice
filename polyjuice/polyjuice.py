#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
docstr = """
Polyjuice

Usage:
    polyjuice.py (-h | --help)
    polyjuice.py [-lzm]  (<input_path> <output_path>) [<config_file>]
    polyjuice.py [-lzc] [<config_file>]

Options:
  -h --help                     Show this message and exit
  -z --zip                      Archives the output folder
  -l --log                      Give progress of program
  -c --config                   Use config file to get input and output paths
  -m --multiple                 The input folder with multiple ISO's
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
import datetime
import time
import progressbar
from docopt import docopt
from filch import DicomCaretaker

CONFIG_PATH = '<config_file>'
INPUT_DIR = '<input_path>'
OUTPUT_DIR = '<output_path>'
ZIP_DIR = '<zip_output_path>'
_print_log = '--log'
_zip_folder = '--zip'
_use_config = '--config'
_use_multiple= '--multiple'

def go_to_library(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except:
        print("Check config file")
        exit()
    return config

def ask_hermione(out_dir):
    print("Lets ask hermione")
    print("Output DIr "+str(out_dir))
    if not os.path.exists(out_dir):
        print("Directory doesn't exist lets create one ")
        try:
            os.makedirs(out_dir)
        except Exception as e:
            raise e

def consult_book(dicom_dir, out_dir, zip_dir, deletions, modifications):
    dicom_file = DicomCaretaker()
    in_dir = dicom_file.start(dicom_dir, out_dir)

    study_date,patient_id = brew_potion(dicom_file, in_dir, out_dir, deletions, modifications, args[_print_log])
    add_hair(study_date, patient_id, out_dir, zip_dir)

    # Checking if the file is ISO
    dicom_file.end()

def brew_potion(dicom_file, in_dir, out_dir, deletions, modifications, verbose):
    count = 0
    for path, subdirs, files in os.walk(in_dir):
        for name in files:
            log_path = os.path.join(out_dir, "log.txt")
            log_file = open(log_path,"a")
            if verbose:
                print(os.path.join(path, name))
            log_file.write(os.path.join(path, name)+"\n")
            try:
                with open(os.path.join(path, name)) as working_file:
                    if verbose:
                        print("Working on {}".format(name))
                    log_file.write("Working on {}".format(name)+"\n")
                    print("Checking Scrub")
                    dataset = dicom_file.scrub(working_file, deletions, modifications, verbose, name, log_file)
                    # Obtaining the Date when MRI Scan has been performed and Use it for Renaming
                    # NACC Convention expects the Output folder Name to be in PatientID_StudyDate format
                    date_item = dataset.data_element('StudyDate').tag
                    patient_item  = dataset.data_element('PatientID').tag
                    if count == 0:
                        study_date = dataset[date_item].value
                        patient_id = dataset[patient_item].value
                        count = count+1
                    print(study_date)
                    # Checking if we can append a recent StudyDate to Patient
                    dicom_file.save_output(dataset, out_dir, name)
            except Exception, e:
                if verbose:
                    print("{} failed".format(name))
                    print (str(e))
                log_file.write("{} failed".format(name)+"\n")
                log_file.write(str(e)+"\n")
            log_file.close()
    return study_date, patient_id

def add_hair(study_date, patient_id, out_dir, zip_dir):
    # Converting study_date in String to desired date format
    desired_study_date = datetime.datetime.strptime(study_date,'%Y%m%d').strftime('%m-%d-%Y')
    renamed_file = patient_id + "_" + desired_study_date
    print(renamed_file)
    # Change the Name of the Output directory
    old_name = os.path.join(out_dir, "DICOM")
    new_name = os.path.join(out_dir, renamed_file)
    shutil.move(old_name, new_name)

    log_name = os.path.join(out_dir, "log.txt")
    new_log_name = os.path.join(out_dir, renamed_file + "_log.txt")
    shutil.move(log_name, new_log_name)
    # Working on converting into ZIP folder
    if(zip_dir):
        shutil.make_archive(new_name, 'zip', new_name)
        ask_hermione(zip_dir)
        os.system("mv {}.zip {}".format(new_name, zip_dir))

def main(args):

    if args[CONFIG_PATH]:
        config_path = args[CONFIG_PATH]
    else: config_path = 'config.yaml'

    config = go_to_library(config_path)
    deletions = config.get('deletions')
    modifications = config.get('modifications')
    if _zip_folder:
        zip_dir = config.get('zip')
        print("zip folder " + str(zip_dir))


    if args[_use_config]:
        #get from config file
        in_root = config.get('in_data_root')
        out_root = config.get('out_data_root')
        io_pairs = config.get('io_pairs')

        #TODO: Find where to put progress bar
        '''bar = progressbar.ProgressBar()
        for i in bar(range(100)):
            time.sleep(2)'''

        for io_pair in io_pairs:
            dicom_dir = os.path.join(in_root, io_pair['input'])
            out_dir = os.path.join(out_root, io_pair['output'])
            ask_hermione(out_dir)
            consult_book(dicom_dir, out_dir, zip_dir, deletions, modifications)

    elif args[_use_multiple]:
        # Looping through each ISO in Directory
        count1 = 0
        iso_file = args[INPUT_DIR]
        print("iso file " + iso_file)
        for current_iso in os.listdir(iso_file):
            count1 = count1 + 1
            print("Going through ISO " + str(count1))
            dicom_dir = os.path.join(iso_file, current_iso)
            if dicom_dir.endswith(".iso"):
                out_dir = args[OUTPUT_DIR]
                ask_hermione(out_dir)
                consult_book(dicom_dir, out_dir, zip_dir, deletions, modifications)
    else:
        dicom_dir = args[INPUT_DIR]
        out_dir = args[OUTPUT_DIR]
        ask_hermione(out_dir)
        consult_book(dicom_dir, out_dir, zip_dir, deletions, modifications)

# Integrating Things with Docopt
if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
