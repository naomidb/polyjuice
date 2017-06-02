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

def main():
    import sys
    if len(sys.argv) != 3:
        #check for proper number of args
        print()
        sys.exit()
    dicom_dir, out_dir = sys.argv[1:]
    flag = False
    if(dicom_dir.endswith(".iso")):
        # Work with ISO Stuff
        flag =  True
        # If user gives ISO then pulling DICOM folder from ISO
        os.system("hdiutil mount %s" % dicom_dir)
        in_dir = "/Volumes/DCS/DICOM"
    else:
        in_dir = os.path.join(dicom_dir, "DICOM")
    # Check in_dir

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

    if flag == True:
        # Unmount
        os.system("hdiutil unmount -force /Volumes/DCS")
if __name__ == '__main__':
    main()
