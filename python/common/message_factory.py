from python.common.plain_text_message import PlainTextMessage
from python.common.encrypted_message import EncryptedMessage


class MessageFactory:

    @staticmethod
    def get_message(encrypt_at_rest: bool, message_encoding: str, log_level: str, encrypt_key=''):
        """
        returns a plain text or encrypted message instance
        :param encrypt_at_rest:
        :param message_encoding:
        :param log_level:
        :param encrypt_key:
        :return:
        """
        if encrypt_at_rest:
            return EncryptedMessage(message_encoding, log_level, encrypt_key)
        return PlainTextMessage(message_encoding, log_level)
