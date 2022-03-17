from http import HTTPStatus

class IdNotFoundError(Exception):
    def __init__(self,id):
        self.message = f"ID {id} not found"
        self.status_code = HTTPStatus.NOT_FOUND

class InvalidKeysError(Exception):
    def __init__(self, invalid_keys, expected_keys):
        self.message = "Invalid keys"
        self.invalid_keys = invalid_keys
        self.expected_keys = expected_keys
        self.status_code = HTTPStatus.BAD_REQUEST

class MissingKeyError(Exception):
    def __init__(self,missing_keys,expected_keys):
        self.message = "Missing keys"
        self.missing_keys = missing_keys
        self.expected_keys = expected_keys
        self.status_code = HTTPStatus.BAD_REQUEST


class TypeValueError(Exception):
    def __init__(self,wrong_field):
        self.wrong_field = wrong_field
        self.status_code = HTTPStatus.BAD_REQUEST
