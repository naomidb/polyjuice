import dicom

class DicomImage(object):

    def __init__(self, dicom_file):
        self._dataset = dicom.read_file(dicom_file)

    def modify_item(self, key, value, delete, log=None):
        _dataset = self._dataset
        if (key in _dataset):
            item = _dataset.data_element(key).tag
            if delete:
                del _dataset[item]
                action = "deleted"
            else:
                item.value = value
                action = "modified"

            if log:
                modify_message = "{} {}".format(key, action)
                log(modify_message)

    def get_value(self, key):
        _dataset = self._dataset
        item = _dataset.data_element(key).tag
        return _dataset[item].value

    def get_study_date(self):
        return self.get_value('StudyDate')

    def get_patient_id(self):
        return self.get_value('PatientID')

    def save_image(self, out):
        _dataset = self._dataset
        _dataset.save_as(out)