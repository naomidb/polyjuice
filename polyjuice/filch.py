import dicom
import os
import os.path
import platform

class DicomCaretaker(object):
    is_iso = False

    def start(self, dicom_dir, out):
        in_dir = dicom_dir
        if(dicom_dir.endswith(".iso")):
            self.is_iso =  True
            # If user gives ISO then mount and pull DICOM folder from ISO
            os.system("mkdir myrtles_bathroom")

            if platform.system() == 'Darwin':
                os.system("hdiutil mount -mountpoint myrtles_bathroom/ISOImage %s" % dicom_dir)
            elif platform.system() == 'Linux':
                os.system("sudo mount -o loop %s myrtles_bathroom/ISOImage" % dicom_dir)

            in_dir = "myrtles_bathroom/ISOImage"
        os.system("mkdir %s/DICOM" % out)
        return in_dir

    def scrub(self, working_file, deletions, modifications, verbose, name,log_file):
        dataset = dicom.read_file(working_file)
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
        if self.is_iso:
            if platform.system() == 'Darwin':
                os.system("hdiutil unmount myrtles_bathroom/ISOImage")
            elif platform.system() == 'Linux':
                os.system("sudo unmount myrtles_bathroom/ISOImage")
            os.system("rmdir myrtles_bathroom")
