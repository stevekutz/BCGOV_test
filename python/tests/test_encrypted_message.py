import pytest
from python.common.encrypted_message import EncryptedMessage
from pprint import pprint


class TestEncryptedMessage:

    BYTE_ENCODING = 'utf-8'
    KEY = 'to1AC3l-KLazylZRYHVTOVq_v7ixfdLeHTXWN5mBVIs='

    @pytest.fixture
    def sample_data(self):
        return {
            'event_id': 1234,
            'event_type': 'vt_query',
            'vt_query': {'ticket_number': '123ABC'}}

    @pytest.fixture
    def encrypted_message(self):
        return EncryptedMessage(TestEncryptedMessage.BYTE_ENCODING, 'DEBUG', TestEncryptedMessage.KEY)

    @pytest.fixture
    def get_encrypted_message(self, sample_data):
        encrypted_message = EncryptedMessage(TestEncryptedMessage.BYTE_ENCODING, 'DEBUG', TestEncryptedMessage.KEY)
        return encrypted_message.encrypt_sensitive_attribute(sample_data)

    @staticmethod
    def test_message_instantiation(encrypted_message):
        assert isinstance(encrypted_message, EncryptedMessage)

    @staticmethod
    def test_encrypt_sensitive_attribute_method(get_encrypted_message):
        assert 'vt_query' not in get_encrypted_message
        assert 'encrypted' in get_encrypted_message
        assert isinstance(get_encrypted_message['encrypted'], str)

    @staticmethod
    def test_decrypt_sensitive_attribute_method(get_encrypted_message, encrypted_message, sample_data):
        decrypted_message = encrypted_message.decrypt_sensitive_attribute(get_encrypted_message)
        assert 'vt_query' in decrypted_message
        assert 'encrypted' not in decrypted_message
        assert 'ticket_number' in decrypted_message['vt_query']
        assert decrypted_message == sample_data

    @staticmethod
    def test_encode_ingested_method(encrypted_message, sample_data):
        message = encrypted_message.encode_ingested_message(sample_data)
        assert isinstance(message, bytes)

    @staticmethod
    def test_decode_ingested_method(encrypted_message, sample_data):
        message_bytes = encrypted_message.encode_ingested_message(sample_data)
        decrypted_message = encrypted_message.decode_ingested_message(message_bytes)
        assert decrypted_message == sample_data

    @staticmethod
    def test_encode_validated_message_without_errors(encrypted_message, sample_data):
        message_bytes = encrypted_message.encode_validated_message(sample_data)
        assert isinstance(message_bytes, bytes)

    @staticmethod
    def test_encode_validated_message_with_errors(encrypted_message, sample_data):
        error_message = {'fieldA': ['required', 'must be string']}
        message_bytes = encrypted_message.encode_validated_message(sample_data, error_message)
        assert isinstance(message_bytes, bytes)
