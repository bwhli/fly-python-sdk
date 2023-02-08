class MissingApiHostnameError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class MissingApiTokenError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
