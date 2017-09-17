
class APIInvalidData(Exception):
    """ an API endpoint has been given invalid data """
    pass

class APIAlreadyExists(Exception):
    """ an API create operation failed because the entry being created already exists """
    def __init__(self, message, id):
        self.message = message
        self.id = id
