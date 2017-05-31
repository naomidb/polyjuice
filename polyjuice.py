import os
import os.path
import dicom
from dicom.errors import InvalidDicomError

def deletion(deletion_pointer):
    del deletion_pointer.RescaleIntercept
    del deletion_pointer.RescaleSlope
    del deletion_pointer.RescaleType
    #use config file for additional deletions

def modification(modification_pointer):
    #use config file for modified values

def main():
    import sys
    if len(sys.argv) != 3:
        #check for proper number of args
        print()
        sys.exit()
    in_dir, out_dir = sys.argv[1:]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for file in os.listdir(in_dir):
        with open(file) as working_file:
            dicom_pointer = dicom.read_file("working_file")
            deletion(dicom_pointer)
            modification(dicom_pointer)

if __name__ == '__main__':
    main()