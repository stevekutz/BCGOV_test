from python.common.message_factory import MessageFactory
from python.common.plain_text_message import PlainTextMessage
from python.common.encrypted_message import EncryptedMessage


class TestMessageFactory:

    SECRET_KEY_SAMPLE = 'to1AC3l-KLazylZRYHVTOVq_v7ixfdLeHTXWN5mBVIs='

    @staticmethod
    def test_plain_text_message_instantiation():
        factory = MessageFactory()
        message = factory.get_message(False, 'utf-8', 'DEBUG')
        assert isinstance(message, PlainTextMessage)

    @staticmethod
    def test_encrypted_message_instantiation():
        factory = MessageFactory()
        message = factory.get_message(True, 'utf-8', 'DEBUG', TestMessageFactory.SECRET_KEY_SAMPLE)
        assert isinstance(message, EncryptedMessage)
