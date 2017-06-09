import dicom
import os
import os.path

class DicomCaretaker(object):
    is_iso = False

    def start(self, dicom_dir, out):
        print("let's sTART")
        in_dir = dicom_dir
        print(dicom_dir)
        if(dicom_dir.endswith(".iso")):
            self.is_iso =  True
            # print("Got your iso")
            # If user gives ISO then mount and pull DICOM folder from ISO
            # OSX only
            os.system("mkdir myrtles_bathroom")
            os.system("hdiutil mount -mountpoint myrtles_bathroom/ISOImage %s" % dicom_dir)
            in_dir = "myrtles_bathroom/ISOImage"
        os.system("mkdir %s/DICOM" % out)
        return in_dir

    def scrub(self, working_file, deletions, modifications, verbose, name,log_file):
        dataset = dicom.read_file(working_file)
        # print("Entered Scrub ")
        # print(dataset[date_item].value)
        self.delete_item(dataset, deletions, working_file, verbose, name,log_file)
        self.modify_item(dataset, modifications, working_file, verbose, name,log_file)
        return dataset

    def delete_item(self, dataset, deletions, working_file, verbose, name,log_file):
        for key in deletions:
            if (key in dataset):
                item = dataset.data_element(key).tag
                del dataset[item]
                if verbose:
                    print ("{} : {} deleted".format(name, key))
                log_file.write("{} : {} deleted".format(name, key)+"\n")

    def modify_item(self, dataset, modifications, working_file, verbose, name,log_file):
        for key in modifications:
            if (key in dataset):
                item = dataset.data_element(key)
                item.value = modifications[key]
                if verbose:
                    print ("{} : {} changed".format(name, key))
                log_file.write("{} : {} changed".format(name, key)+"\n")

    def save_output(self, dataset, out, filename):
        output = os.path.join(out, "DICOM", filename)
        dataset.save_as(output)

    def end(self):
        # OSX only
        if self.is_iso:
            os.system("hdiutil unmount myrtles_bathroom/ISOImage")
            os.system("rmdir myrtles_bathroom")
