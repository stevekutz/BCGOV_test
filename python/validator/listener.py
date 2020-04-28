from python.validator.config import Config
from python.validator.validator import Validate
from python.common.rabbitmq import RabbitMQ
from python.common.message_factory import MessageFactory
import logging


class Listener:
    """
        This listener watches the RabbitMQ WATCH_QUEUE defined in the
        Config.  When a message appears in the queue the Listener:
         - invokes callback(),
         - determines whether the message is valid or not valid,
         - writes the message to a valid or not valid queue
    """
    def __init__(self, config, validator, rabbit_writer, rabbit_listener, message):
        self.validator = validator
        self.config = config
        self.writer = rabbit_writer
        self.listener = rabbit_listener
        self.message = message

        logging.basicConfig(level=config.LOG_LEVEL)
        logging.warning('*** validator initialized  ***')

    def main(self):
        """
            Start listening for messages on the WATCH_QUEUE
            when a message arrives invoke the callback()
        :return:
        """
        self.listener.consume(self.config.WATCH_QUEUE, self.callback)

    def callback(self, ch, method, properties, body):
        logging.info('message received; callback invoked')

        message_dict = self.message.decode_ingested_message(body)

        result = self.validator.validate(message_dict)
        if result['isSuccess']:
            # Validation SUCCESSFUL
            logging.info("write to: " + self.config.VALID_QUEUE)
            if self.writer.publish(self.config.VALID_QUEUE, self.message.encode_validated_message(message_dict)):
                ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            # Validation FAILED
            logging.info("write to: " + self.config.FAIL_QUEUE)
            if self.writer.publish(
                    self.config.FAIL_QUEUE,
                    self.message.encode_validated_message(message_dict, result)):
                ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    Listener(
        Config(),
        Validate(Config()),
        RabbitMQ(
            Config.VALIDATOR_USER,
            Config.VALIDATOR_PASS,
            Config.RABBITMQ_URL,
            Config.LOG_LEVEL,
            Config.MAX_CONNECTION_RETRIES,
            Config.RETRY_DELAY),
        RabbitMQ(
            Config.VALIDATOR_USER,
            Config.VALIDATOR_PASS,
            Config.RABBITMQ_URL,
            Config.LOG_LEVEL,
            Config.MAX_CONNECTION_RETRIES,
            Config.RETRY_DELAY),
        MessageFactory.get_message(
            Config.ENCRYPT_AT_REST,
            Config.RABBITMQ_MESSAGE_ENCODE,
            Config.LOG_LEVEL,
            Config.ENCRYPT_KEY)
    ).main()
