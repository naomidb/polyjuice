#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
docstr = """
Polyjuice

Usage:
    polyjuice.py (-h | --help)
    polyjuice.py [-z] (<input_path> <output_path>) [-z <zip_output_path>]
    polyjuice.py [-l | --log] (<input_path> <output_path>) [-c <config_file>] [-z <zip_output_path>]
    polyjuice.py [-l | --log] [-c <config_file>] [-z <zip_output_path>]

Options:
  -h --help                                     Show this message and exit
  -z --zip                                      Archives the output folder
  -l --log                                      Give progress of program
  -c --config                                   Give path to config file

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
from docopt import docopt
from filch import DicomCaretaker

CONFIG_PATH = '<config_file>'
INPUT_DIR = '<input_path>'
OUTPUT_DIR = '<output_path>'
ZIP_DIR = '<zip_output_path>'
_print_log = '--log'

def consult_book(out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

def raid_snapes_cupboard(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except:
        print("Check config file")
        exit()
    return config

def brew_potion(dicom_file, in_dir, out_dir, deletions, modifications, verbose):
    count = 0
    for path, subdirs, files in os.walk(in_dir):
        for name in files:
            print os.path.join(path, name)
            try:
                with open(os.path.join(path, name)) as working_file:
                    if verbose:
                        print("Working on {}".format(name))
                    dataset = dicom_file.scrub(working_file, deletions, modifications, verbose)
                    # Obtaining the Date when MRI Scan has been performed and Use it for Renaming
                    # NACC Convention expects the Output folder Name to be in PatientID_StudyDate format
                    date_item = dataset.data_element('StudyDate').tag
                    patient_item  = dataset.data_element('PatientID').tag
                    if count == 0:
                        study_date = dataset[date_item].value
                        patient_id = dataset[patient_item].value
                        count = count+1
                    # Checking if we can append a recent StudyDate to Patient
                    # print study_date
                    # print patient_id
                    dicom_file.save_output(dataset, out_dir, name)
            except Exception, e:
                print("{} failed".format(name))
                print (str(e))
    return study_date,patient_id

def main(args):
    if args[CONFIG_PATH]:
        config_path = args[CONFIG_PATH]
    else: config_path = 'config.yaml'
    dicom_dir = args[INPUT_DIR]
    out_dir = args[OUTPUT_DIR]
    consult_book(out_dir)

    dicom_file = DicomCaretaker()

    in_dir = dicom_file.start(dicom_dir)

    config = raid_snapes_cupboard(config_path)
    deletions = config.get('deletions')
    modifications = config.get('modifications')

    study_date,patient_id = brew_potion(dicom_file, in_dir, out_dir, deletions, modifications, args[_print_log])
    # Converting study_date in String to desired date format
    desired_study_date = datetime.datetime.strptime(study_date,'%Y%m%d').strftime('%m-%d-%Y')
    renamed_file = patient_id + "_" + desired_study_date
    print renamed_file
    # Change the Name of the Output directory
    shutil.move(out_dir, renamed_file)
    # renamed_out_dir = os.rename(out_dir,renamed_file)
    # Working on converting into ZIP folder
    if(args.get(ZIP_DIR)):
        # zip_folder = os.path.join(out_dir, 'DICOM')
        shutil.make_archive(renamed_file, 'zip',renamed_file)

    # Checking if the file is ISO
    dicom_file.end()

# Integrating Things with Docopt
if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
