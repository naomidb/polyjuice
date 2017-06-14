class Lumberjack(object):

    def __init__(self, filepath='log.txt', is_verbose=None):
        self.is_verbose = is_verbose
        self.filepath = filepath

    def __call__(self, message):
        with open(self.filepath, "a+") as log:
            log.write(message + "\n")
        if self.is_verbose:
            print(message)