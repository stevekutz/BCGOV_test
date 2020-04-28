import logging
import json
import datetime


class PlainTextMessage:

    def __init__(self, message_encoding, log_level):
        self.message_encoding = message_encoding
        logging.basicConfig(level=log_level)

    def encode_ingested_message(self, message: dict) -> bytes:
        return self.encode(message)

    def decode_ingested_message(self, body: bytes) -> dict:
        return self.decode(body)

    def encode_validated_message(self, message: dict, errors: dict = None) -> bytes:
        if errors:
            message = self.add_error_to_message(message, errors)
        return self.encode(message)

    def decode_validated_message(self, body: bytes) -> dict:
        return self.decode(body)

    def encode(self, message: dict) -> bytes:
        """
        Encrypt the entire message
        :param message: 
        :return: 
        """
        return bytes(json.dumps(message), self.message_encoding)

    def decode(self, body: bytes) -> dict:
        """
        Decrypt the entire message
        :param body: 
        :return: 
        """
        message_string = body.decode(self.message_encoding)
        return json.loads(message_string)

    @staticmethod
    def add_error_to_message(message, error) -> dict:
        """
            Add 'errors' as a message attribute so as to keep a
            history of events in case it fails repeatedly.
        :param message:
        :param error:
        :return:
        """
        now_string = datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        if not isinstance(message, dict):
            message = dict()

        if 'errors' not in message:
            message['errors'] = []
        message['errors'].append({'description': error, 'timestamp': now_string})
        return message
