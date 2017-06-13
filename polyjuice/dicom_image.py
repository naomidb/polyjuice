import dicom

class DicomImage(object):

    def __init__(self, dicom_file):
        self.dataset = dicom.read_file(dicom_file)

    def modify_item(self, key, value, log=None):
        dataset = self.dataset
        if (key in dataset):
            item = dataset.data_element(key).tag
            item.value = value

            if log:
                modify_message = "{} modified".format(key)
                log(modify_message)

    def delete_item(self, key, log=None):
        dataset = self.dataset
        if (key in dataset):
            item = dataset.data_element(key).tag
            del dataset[item]

            if log:
                delete_message = "{} deleted".format(key)
                log(delete_message)

    def get_value(self, key):
        dataset = self.dataset
        item = dataset.data_element(key).tag
        return dataset[item].value

    def save_image(self, out):
        dataset = self.dataset
        dataset.save_as(out)