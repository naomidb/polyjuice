import os
import json
from copy import copy
import md5
import base64

import dicom

class DicomImage(object):

    def __init__(self, dicom_file):
        self._dataset = dicom.read_file(dicom_file)
        self.filepath = dicom_file.name

    def serialize_metadata(self, **kwargs):
        metadata = {}
        for key in self._dataset.dir():
            element = self._dataset.data_element(key)
            if key != 'PixelData':
                if not element:
                    metadata[key] = None
                else:
                    metadata[key] = self._process_data_element(element)
            else:
                # Dont serialize the pixel data since it isnt metadata
                pass
        return json.dumps(metadata, **kwargs)

    def _process_data_element(self, element):
        type_string = str(type(element))
        if 'Sequence' in type_string or 'length' in repr(element) or type_string == type([]):
            return [self._process_data_element(item) for item in element]
        elif 'Dataset' in type_string:
            elements = [(key, element.data_element(key)) for key in element.dir()]
            metadata = {}
            for key, val in elements:
                metadata[key] = self._process_data_element(val)
            return metadata
        else:
            return str(element._value)

    def _md5ify(self, item):
        m = md5.new()
        m.update(item)
        return base64.b64encode(m.digest)

    def modify_item(self, key, value, delete=False, log=None, obfuscate=False):
        """
        Changes the value of a key value pair in the dataset.

        If delete is supplied the key value pair will be deleted.

        If obfuscate is supplied the value will be the MD5 hash to keep 1 to 1
        relationships around. The main purpose of this is to make sure that we
        can tell if dicom slices come in a series
        """
        _dataset = self._dataset
        if (key in _dataset):
            #Get the Key and Value
            tag_number = _dataset.data_element(key).tag
            if delete:
                del _dataset[tag_number]
                action = "deleted"
            elif obfuscate:
                _dataset[tag_number].value = self._md5ify(value)
                action = "obfuscated"
            else:
                _dataset[tag_number].value = value
                action = "modified"

            if log:
                modify_message = "{}: {} {}".format(self.filepath, key, action)
                log(modify_message)

    def update_patient_id(self, id_pairs, log):
        """
        We need to clean the patient ID by mapping for deidentification purposes.

        if the key __ALL__ exists in the id_pairs dictionary then use that for
        the id mapping
        """
        _dataset = self._dataset
        patient_id = self.get_patient_id()
        for key, val in id_pairs.iteritems():
            if(patient_id == key or key == '__ALL__'):
                new_id = val
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
        self._dataset.save_as(out)
