import json
from abc import ABC, abstractmethod
from json.decoder import JSONDecodeError


class JsonDocumentParser(ABC):
    is_request_of_type = False
    object_type = ""

    def __init__(self, raw_json):
        self.raw_json = raw_json
        self.valid_json = False
        try:
            self.data = json.loads(self.raw_json)
        except JSONDecodeError as err:
            raise Exception(f"Could not parse Json input, error msg: {err}")
        else:
            self.valid_json = True

    def is_valid_json(self):
        return self.valid_json

    def is_of_type(self):
        return self.is_request_of_type

    def get_object_type(self):
        return self.object_type

    def get_attribute(self, attr_name):
        return self.data[attr_name]

    @abstractmethod
    def determine_document_is_of_type(self):
        raise NotImplementedError
