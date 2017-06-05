import dicom
import os
import os.path

class DicomImage(object):
    is_iso = False

    def start(self, input):
        if(dicom_dir.endswith(".iso")):
        is_iso =  True
        # If user gives ISO then mount and pull DICOM folder from ISO
        # OSX only
        os.system("hdiutil mount %s" % dicom_dir)
        in_dir = "/Volumes/DCS/DICOM"
        else:
            in_dir = os.path.join(dicom_dir, "DICOM")
        return in_dir

    def delete_item(self, dataset, kill_list):
        for key in kill_list:
            if (key in dataset):
                item = dataset.data_element(key).tag
                del dataset[item]
                print ("{} deleted".format(key))

    def modify_item(self, dataset, changes):
        for key in changes:
            if (key in dataset):
                item = dataset.data_element(key)
                item.value = changes[key]
                print ("{} changed".format(key))

    def end(self):
        # OSX only
        if is_iso:
            os.system("hdiutil unmount /Volumes/DCS")