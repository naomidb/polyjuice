import os
import os.path
import dicom
from dicom.errors import InvalidDicomError
import yaml
from docopt import docopt

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
        ingredient = deletion_pointer.data_element(key).tag
        del deletion_pointer[ingredient]
        print ("{} deleted".format(key))

def modification(modification_pointer, modify_me):
    #use dictionary from config file
    for key in modify_me:
        ingredient = modification_pointer.data_element(key)
        ingredient.value = modify_me[key]
        print ("{} changed".format(key))

def brew(dataset, out, filename):
    output = os.path.join(out, filename)
    dataset.save_as(output)
    #TODO: Files may not be saving to the right format. Need to test in Windows.

def main():
    import sys
    if len(sys.argv) != 3:
        #check for proper number of args
        print()
        sys.exit()
    in_dir, out_dir = sys.argv[1:]

    config = raid_snapes_cupboard()
    delete_me = config.get('deletions')
    modify_me = config.get('modifications')

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for file in os.listdir(in_dir):
        try: 
            with open(os.path.join(in_dir, file)) as working_file:
                dicom_pointer = dicom.read_file(working_file, force=True)
                print("Working on {}".format(file))
                print(dicom_pointer)
                deletion(dicom_pointer, delete_me)
                modification(dicom_pointer, modify_me)
                brew(dicom_pointer, out_dir, file)
        except Exception, e:
            print (file)
            print (str(e))

if __name__ == '__main__':
    main()