import dicom
import os
import os.path

class DicomCaretaker(object):
    is_iso = False

    def start(self, dicom_dir):
        if(dicom_dir.endswith(".iso")):
            self.is_iso =  True
            # If user gives ISO then mount and pull DICOM folder from ISO
            # OSX only
            os.system("hdiutil mount %s" % dicom_dir)
            in_dir = "/Volumes/DCS/DICOM"
        else:
            in_dir = os.path.join(dicom_dir, "DICOM")
        return in_dir

    def scrub(self, working_file, deletions, modifications, verbose):
        dataset = dicom.read_file(working_file)
        self.delete_item(dataset, deletions, verbose)
        self.modify_item(dataset, modifications, verbose)
        return dataset

    def delete_item(self, dataset, deletions, verbose):
        for key in deletions:
            if (key in dataset):
                item = dataset.data_element(key).tag
                del dataset[item]
                if verbose:
                    print ("{} deleted".format(key))

    def modify_item(self, dataset, modifications, verbose):
        for key in modifications:
            if (key in dataset):
                item = dataset.data_element(key)
                item.value = modifications[key]
                if verbose:
                    print ("{} changed".format(key))

    def save_output(self, dataset, out, filename):
        output = os.path.join(out, filename)
        dataset.save_as(output)

    def end(self):
        # OSX only
        if self.is_iso:
            os.system("hdiutil unmount /Volumes/DCS")