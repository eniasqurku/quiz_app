from rest_framework.exceptions import APIException


class InvalidData(Exception):
    def __init__(self, message):
        self.message = message

    def get_message(self):
        return self.message


class APIException202(APIException):
    status_code = 202

    def __init__(self, message, obj):
        self.message = message
        self.obj = obj
