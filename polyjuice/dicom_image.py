import dicom

class DicomImage(object):

    def __init__(self, dicom_file):
        self.dataset = dicom.read_file(dicom_file)

    def modify_item(self, key, value):
        dataset = self.dataset
        if (key in dataset):
            item = dataset.data_element(key).tag
            item.value = value

    def delete_item(self, key):
        dataset = self.dataset
        if (key in dataset):
            item = dataset.data_element(key).tag
            del dataset[item]

    def get_value(self, key):
        dataset = self.dataset
        item = dataset.data_element(key).tag
        return dataset[item].value

    def save_image(self, out):
        dataset = self.dataset
        dataset.save_as(out)