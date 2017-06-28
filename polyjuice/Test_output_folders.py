import unittest
import sys
import yaml
import csv
import os
from polyjuice import browse_restricted_section
from lumberjack import Lumberjack

config_path = 'test_config.yaml'
main_config_path = '/Users/amineni95/Desktop/Projects/polyjuice/polyjuice/config.yaml'
log_path = '/Users/amineni95/Desktop/Output/log.txt'
expected_output_files = '/Users/amineni95/Desktop/Output/output.csv'
class check_outputfile_path(unittest.TestCase):
    def test_lookupfile_exists(self):
        try:
            with open(config_path, 'r') as config_file:
                config = yaml.load(config_file.read())
                parent_file = config.get('input_path')
                out_dir = config.get('output_path')
                zip_dir = config.get('zip_path')
                id_pairs = {}
                # log = 'log.txt'
        except:
            print("Error: Check config file")
            exit()

        try:
            with open(main_config_path, 'r') as config_file:
                modify_config = yaml.load(config_file.read())
                modifications = modify_config.get('modifications')
        except Exception as e:
            print("Can't find Modifications Config")

        print log_path
        log = Lumberjack(log_path, None)
        browse_restricted_section(parent_file, out_dir, zip_dir, modifications, id_pairs, log)
        poly_dirs=[]
        poly_dirs = [f for f in sorted(os.listdir(out_dir)) if not f.startswith('.')]

        print poly_dirs
        real_list = []
        with open(expected_output_files, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                real_list.append(row)
        expected_list = [item for sublist in real_list for item in sublist]
        print expected_list
        self.assertListEqual(poly_dirs.sort() ,expected_list.sort())
unittest.main()
