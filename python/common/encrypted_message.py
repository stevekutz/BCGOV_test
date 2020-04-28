from cryptography.fernet import Fernet
from python.common.plain_text_message import PlainTextMessage
from pprint import pprint


class EncryptedMessage(PlainTextMessage):

    FERNET_MESSAGE_ENCODING = 'utf-8'
    ENCRYPTED_ATTRIBUTE_NAME = 'encrypted'

    def __init__(self, message_encoding: str, log_level: str, encrypt_key: str):
        super().__init__(message_encoding, log_level)
        self.fernet = Fernet(bytes(encrypt_key, EncryptedMessage.FERNET_MESSAGE_ENCODING))

    def encode_ingested_message(self, message: dict) -> bytes:
        """
        Encrypt and encode the entire message.  When a message is
        ingested it hasn't yet been validated so we encrypt the
        entire message before sending it to RabbitMQ in case the
        message format isn't as expected.
        :param message:
        :return:
        """
        return self.fernet.encrypt(self.encode(message))

    def decode_ingested_message(self, token: bytes) -> dict:
        """
        Decrypt and decode an ingested message are return a Python dictionary.
        An ingested message is entirely encrypted.
        :param token:
        :return:
        """
        return self.decode(self.fernet.decrypt(token))

    def encode_validated_message(self, message: dict, errors=None) -> bytes:
        """
        Encrypt the sensitive attributes of the message but leave the event attributes and
        errors attributes unencrypted so admins can look at the message in RabbitMQ and
        determine why the message failed validation or why it couldn't be written to the
        database.
        :param message:
        :param errors:
        :return:
        """
        if errors:
            message = self.add_error_to_message(message, errors)
        message = self.encrypt_sensitive_attribute(message)
        return self.encode(message)

    def decode_validated_message(self, body: bytes) -> dict:
        decoded_message = self.decode(body)
        return self.decrypt_sensitive_attribute(decoded_message)

    def encrypt_sensitive_attribute(self, message: dict) -> dict:
        """
        Encrypt the attribute of the message that may contain personal information
        and return the entire message with encrypted and unencrypted attributes.
        The event attributes and errors attributes are left unencrypted to help
        administrators troubleshoot validation errors .
        :param message:
        :return:
        """
        sensitive_attribute = message['event_type']
        sensitive_bytes = self.encode(message[sensitive_attribute])
        encrypted_string = self.fernet.encrypt(sensitive_bytes).decode(EncryptedMessage.FERNET_MESSAGE_ENCODING)
        message[EncryptedMessage.ENCRYPTED_ATTRIBUTE_NAME] = encrypted_string
        message.pop(sensitive_attribute)
        return message

    def decrypt_sensitive_attribute(self, message: dict) -> dict:
        """
        Decrypt the `encrypted` message attribute within the message and return the
        original message with the unencrypted message attributes included.
        :param message:
        :return:
        """
        sensitive_attribute = message['event_type']
        token = message[EncryptedMessage.ENCRYPTED_ATTRIBUTE_NAME].encode(EncryptedMessage.FERNET_MESSAGE_ENCODING)
        sensitive_bytes = self.fernet.decrypt(token)
        message[sensitive_attribute] = self.decode(sensitive_bytes)
        message.pop(EncryptedMessage.ENCRYPTED_ATTRIBUTE_NAME)
        return message
