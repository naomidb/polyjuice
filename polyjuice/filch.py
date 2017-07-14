import os
import os.path
import platform
import datetime
import time

class DicomCaretaker(object):
    is_iso = False
    mount_location = "myrtles_bathroom"

    def mount_iso(self, iso_path, out):
        self.is_iso =  True
        mount_point = self.mount_location + "/ISOImage"
        # If user gives ISO then mount and pull DICOM folder from ISO
        os.system("mkdir %s" % self.mount_location)
        if platform.system() == 'Darwin':
            os.system("hdiutil mount -mountpoint {} {}".format(mount_point, iso_path))
        elif platform.system() == 'Linux':
            os.system("sudo mount -o loop {} {}".format(iso_path, mount_point))

        return mount_point

    def scrub(self, image, modifications, id_pairs, log):
        for key, value in modifications.items():
            delete = True if value == None else False
            image.modify_item(key, value, delete, log)

        image.update_patient_id(id_pairs, log)

    def get_folder_name(self, image):
        study_date = image.get_study_date()
        patient_id = image.get_patient_id()

        #Change study_date to desired format
        desired_study_date = datetime.datetime.strptime(study_date,'%Y%m%d').strftime('%m_%d_%Y')
        #Rename according to NACC conventions
        folder_name = patient_id + "_" + desired_study_date
        return folder_name

    def save_output(self, image, identified_folder, filename):
        output = os.path.join(identified_folder, filename)
        image.save_image(output)

    def unmount_iso(self):
        mount_location = self.mount_location
        if self.is_iso:
            if platform.system() == 'Darwin':
                os.system("hdiutil unmount %s/ISOImage" % mount_location)
            elif platform.system() == 'Linux':
                os.system("sudo unmount %s/ISOImage" % mount_location)
            os.system("rmdir %s" % mount_location)
