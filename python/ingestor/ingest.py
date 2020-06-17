from python.common.helper import load_json_into_dict
from python.ingestor.config import Config
from python.common.rabbitmq import RabbitMQ
from python.common.message_factory import MessageFactory
from flask import request, jsonify, Response
from flask_api import FlaskAPI
import xmltodict
import logging


application = FlaskAPI(__name__)
logging.basicConfig(level=Config.LOG_LEVEL)
logging.warning('*** ingestor initialized ***')

rabbit_mq = RabbitMQ(
        Config.INGEST_USER,
        Config.INGEST_PASS,
        Config.RABBITMQ_URL,
        Config.LOG_LEVEL,
        Config.MAX_CONNECTION_RETRIES,
        Config.RETRY_DELAY)

available_parameters = load_json_into_dict('python/ingestor/' + Config.PARAMETERS_FILE)


@application.route('/v1/publish/event/<data_type>', methods=["POST"])
@application.route('/v1/publish/event', methods=["POST"])
def create(data_type='ETK'):

    if data_type not in available_parameters:
        message = data_type + ' is a not a valid parameter'
        logging.warning(message)
        return jsonify({"error": message}), 500

    message = MessageFactory.get_message(
        available_parameters[data_type]['encrypt-at-rest'],
        Config.RABBITMQ_MESSAGE_ENCODE,
        Config.LOG_LEVEL,
        Config.ENCRYPT_KEY)

    logging.warning('content-type: ' + request.content_type)
    if request.content_type == "application/json":
        payload = request.json
    if request.content_type == "application/xml":
        payload = xmltodict.parse(request.get_data())
    logging.warning('payload type: ' + str(type(payload)))

    if rabbit_mq.publish(available_parameters[data_type]['queue'],
                         message.encode_ingested_message(payload)):
        return jsonify(payload), 200
    else:
        return Response('Unavailable', 500, mimetype='application/json')


if __name__ == "__main__":
    application.run(host='0.0.0.0')
