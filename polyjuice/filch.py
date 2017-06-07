import dicom
import os
import os.path

class DicomCaretaker(object):
    is_iso = False

    def start(self, dicom_dir, out):
        in_dir = dicom_dir
        if(dicom_dir.endswith(".iso")):
            self.is_iso =  True
            # If user gives ISO then mount and pull DICOM folder from ISO
            # OSX only
            os.system("mkdir myrtles_bathroom")
            os.system("hdiutil mount -mountpoint myrtles_bathroom/ISOImage %s" % dicom_dir)
            in_dir = "myrtles_bathroom/ISOImage"
        os.system("mkdir %s/DICOM" % out)
        return in_dir

    def scrub(self, working_file, deletions, modifications, verbose, name):
        dataset = dicom.read_file(working_file)
        self.delete_item(dataset, deletions, working_file, verbose, name)
        self.modify_item(dataset, modifications, working_file, verbose, name)
        return dataset

    def delete_item(self, dataset, deletions, working_file, verbose, name):
        for key in deletions:
            if (key in dataset):
                item = dataset.data_element(key).tag
                del dataset[item]
                if verbose:
                    print ("{} : {} deleted".format(name, key))

    def modify_item(self, dataset, modifications, working_file, verbose, name):
        for key in modifications:
            if (key in dataset):
                item = dataset.data_element(key)
                item.value = modifications[key]
                if verbose:
                    print ("{} : {} changed".format(name, key))

    def save_output(self, dataset, out, filename):
        output = os.path.join(out, "DICOM", filename)
        dataset.save_as(output)

    def end(self):
        # OSX only
        if self.is_iso:
            os.system("hdiutil unmount myrtles_bathroom/ISOImage")
            os.system("rmdir myrtles_bathroom")