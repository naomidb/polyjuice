import pydicom

class DicomImage(object):

    def __init__(self, dicom_file):
        self._dataset = pydicom.read_file(dicom_file)
        self.filepath = dicom_file.name

    def modify_item(self, key, value, delete, log=None):
        _dataset = self._dataset
        if (key in _dataset):
            tag_number = _dataset.data_element(key).tag
            if delete:
                del _dataset[tag_number]
                action = "deleted"
            else:
                _dataset[tag_number].value = value
                action = "modified"

            if log:
                modify_message = "{}: {} {}".format(self.filepath, key, action)
                log(modify_message)

    def update_patient_id(self, id_pairs, log):
        _dataset = self._dataset
        patient_id = self.get_patient_id()
        for key in id_pairs:
            if(patient_id == key):
                new_id = id_pairs.get(patient_id)
                id_message = "{}: New ID: {}".format(self.filepath, new_id)
                log(id_message)
                self.modify_item('PatientID', new_id, False, log)
                return None
            elif(patient_id == id_pairs.get(key)):
                return None
        return patient_id

    def get_value(self, key):
        _dataset = self._dataset
        tag_number = _dataset.data_element(key).tag
        return _dataset[tag_number].value

    def get_study_date(self):
        return self.get_value('StudyDate')

    def get_patient_id(self):
        return self.get_value('PatientID')

    def save_image(self, out):
        _dataset = self._dataset
        _dataset.save_as(out)
