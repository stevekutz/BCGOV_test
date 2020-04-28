from python.common.plain_text_message import PlainTextMessage
import pytest
from pprint import pprint


class TestPlainTextMessage:

    BYTE_ENCODING = 'utf-8'

    @pytest.fixture
    def sample_message_dict(self):
        return {
            "attribute_1": "attribute"
        }

    @staticmethod
    def plain_text_message():
        return PlainTextMessage(TestPlainTextMessage.BYTE_ENCODING, 'DEBUG')

    def test_message_instantiation(self):
        message = self.plain_text_message()
        assert isinstance(message, PlainTextMessage)

    def test_plain_message_encode(self, sample_message_dict):
        message = self.plain_text_message()
        encoded_message = message.encode(sample_message_dict)
        assert isinstance(encoded_message, bytes)

    def test_plain_message_decode(self):
        message = self.plain_text_message()
        message_bytes = bytes('{"attribute": "value"}', TestPlainTextMessage.BYTE_ENCODING)
        encoded_message = message.decode(message_bytes)
        assert isinstance(encoded_message, dict)

    @staticmethod
    def test_add_error_to_message_method():
        message_dict = {'event_type': 'some invalid event'}
        expected_error_message = 'error message'
        error_dict = {'isSuccess': False, 'errors': expected_error_message}
        modified_message = PlainTextMessage.add_error_to_message(message_dict, error_dict['errors'])
        assert isinstance(modified_message, dict)
        assert 'errors' in modified_message
        assert 'timestamp' in modified_message['errors'][0]
        assert 'description' in modified_message['errors'][0]
        assert modified_message['errors'][0]['description'] == expected_error_message

    @staticmethod
    def test_add_error_to_message_method_handles_cerberus_errors():
        error_message = {'fieldA': ['required', 'must be string']}
        message_dict = 'some string that is not valid JSON'
        error_dict = {'isSuccess': False, 'errors': error_message}
        modified_message = PlainTextMessage.add_error_to_message(message_dict, error_dict['errors'])
        assert isinstance(modified_message, dict)
        assert 'errors' in modified_message
        assert 'timestamp' in modified_message['errors'][0]
        assert 'description' in modified_message['errors'][0]

    @staticmethod
    def test_encode_validated_message_without_errors(sample_message_dict):
        message = PlainTextMessage('utf-8', 'DEBUG')
        message_bytes = message.encode_validated_message(sample_message_dict)
        assert isinstance(message_bytes, bytes)

    @staticmethod
    def test_encode_validated_message_with_errors(sample_message_dict):
        message = PlainTextMessage('utf-8', 'DEBUG')
        error_message = {'fieldA': ['required', 'must be string']}
        message_bytes = message.encode_validated_message(sample_message_dict, error_message)
        assert isinstance(message_bytes, bytes)
