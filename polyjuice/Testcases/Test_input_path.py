import unittest
import sys
import os
import yaml
config_path = '/Users/amineni95/Desktop/Projects/polyjuice/polyjuice/Testcases/test_config.yaml'
class check_inputfile_path(unittest.TestCase):
    def test_lookupfile_exists(self):
        try:
            with open(config_path, 'r') as config_file:
                config = yaml.load(config_file.read())
        except:
            print("Error: Check config file")
            exit()
        self.assertTrue(os.path.exists(config.get('input_path')))


unittest.main()
