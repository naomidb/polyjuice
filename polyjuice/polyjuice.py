#! /Library/Frameworks/Python.framework/Versions/2.7/bin/python
docstr = """
Polyjuice

Usage:
    polyjuice.py (-h | --help)
    polyjuice.py (<input_path> <output_path>) [<zip_output_path>]
    polyjuice.py [-l] (<input_path> <output_path>)
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

def raid_snapes_cupboard(config_path, dicom_file):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except:
        print("Check config file")
        dicom_file.end()
        exit()
    return config

def brew_potion(dicom_file, in_dir, out_dir, deletions, modifications, verbose):
    count = 0
    for path, subdirs, files in os.walk(in_dir):
        for name in files:
            log_path = os.path.join(out_dir, "log.txt")
            log_file = open(log_path,"a")
            if verbose:
                print os.path.join(path, name)
            log_file.write(os.path.join(path, name)+"\n")
            try:
                with open(os.path.join(path, name)) as working_file:
                    if verbose:
                        print("Working on {}".format(name))
                    log_file.write("Working on {}".format(name)+"\n")
                    dataset = dicom_file.scrub(working_file, deletions, modifications, verbose, name,log_file)
                    # Obtaining the Date when MRI Scan has been performed and Use it for Renaming
                    # NACC Convention expects the Output folder Name to be in PatientID_StudyDate format
                    date_item = dataset.data_element('StudyDate').tag
                    patient_item  = dataset.data_element('PatientID').tag
                    if count == 0:
                        study_date = dataset[date_item].value
                        patient_id = dataset[patient_item].value
                        count = count+1
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
    print renamed_file
    # Change the Name of the Output directory
    old_name = os.path.join(out_dir, "DICOM")
    new_name = os.path.join(out_dir, renamed_file)
    shutil.move(old_name, new_name)
    # Working on converting into ZIP folder
    if(zip_dir):
        shutil.make_archive(new_name, 'zip', new_name)
        os.system("mv {}.zip {}".format(new_name, zip_dir))

def main(args):
    if args[CONFIG_PATH]:
        config_path = args[CONFIG_PATH]
    else: config_path = 'config.yaml'
    dicom_dir = args[INPUT_DIR]
    out_dir = args[OUTPUT_DIR]
    zip_dir = args[ZIP_DIR]
    consult_book(out_dir)

    dicom_file = DicomCaretaker()

    in_dir = dicom_file.start(dicom_dir, out_dir)

    config = raid_snapes_cupboard(config_path, dicom_file)
    deletions = config.get('deletions')
    modifications = config.get('modifications')

    study_date,patient_id = brew_potion(dicom_file, in_dir, out_dir, deletions, modifications, args[_print_log])
    add_hair(study_date, patient_id, out_dir, zip_dir)

    # Checking if the file is ISO
    dicom_file.end()

# Integrating Things with Docopt
if __name__ == '__main__':
    args = docopt(docstr)
    main(args)
