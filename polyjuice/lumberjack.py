import datetime
import os.path

class Lumberjack(object):

    def __init__(self, filepath='log.txt', is_verbose=None):
        self.is_verbose = is_verbose

        filename = os.path.basename(filepath)
        date = str(datetime.date.today())
        name = date + '_' + filename
        path = os.path.dirname(filepath)
        self.log_path = os.path.join(path, name)

        sep = '#' * 10
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_message = sep + " " + timestamp + " " + sep
        self.__call__(time_message)
        self.__call__(sep + sep + sep)


    def __call__(self, message):
        with open(self.log_path, "a+") as log:
            log.write(message + "\n")
        if self.is_verbose:
            print(message)
