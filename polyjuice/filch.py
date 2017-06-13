import os
import os.path
import platform
import datetime

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
        return in_dir

    def scrub(self, dataset, modifications):
        for key in modifications:
            if modifications[key] == None:
                dataset.delete_item(key)
            else:
                dataset.modify_item(key, modifications[key])

    def get_folder_name(self, dataset):
        study_date = dataset.get_value('StudyDate')
        patient_id = dataset.get_value('PatientID')

        #Change study_date to desired format
        desired_study_date = datetime.datetime.strptime(study_date,'%Y%m%d').strftime('%m-%d-%Y')
        #Rename according to NACC conventions
        folder_name = patient_id + "_" + desired_study_date
        return folder_name

    def save_output(self, dataset, identified_folder, filename):
        output = os.path.join(identified_folder, filename)
        dataset.save_image(output)

    def end(self):
        if self.is_iso:
            if platform.system() == 'Darwin':
                os.system("hdiutil unmount myrtles_bathroom/ISOImage")
            elif platform.system() == 'Linux':
                os.system("sudo unmount myrtles_bathroom/ISOImage")
            os.system("rmdir myrtles_bathroom")
