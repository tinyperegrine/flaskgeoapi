class APIException(Exception):

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = 400
        self.payload = payload

    def to_dict(self):
        rv = {'message': self.message, 'payload': self.payload}
        return rv
