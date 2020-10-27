from python.common.message import encode_message
from python.writer.config import Config
import requests
import logging
import json

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def publish_to_fail_queue(**args) -> tuple:
    config = args.get('config')
    message_with_errors = args.get('message')
    writer = args.get('writer')
    is_success = writer.publish(config.FAIL_QUEUE, encode_message(message_with_errors, config.ENCRYPT_KEY))
    return is_success, args


def build_payload_to_send_to_geocoder(**args) -> tuple:
    m = args.get('message')
    event_type = m['event_type']
    args['payload'] = dict({
        "address": m[event_type]['violation_highway_desc']
    })
    return True, args


def callout_to_geocoder_api(**args) -> tuple:
    config = args.get('config')
    endpoint = config.GEOCODER_API_URI
    payload = args.get('payload')
    logging.info('Geocoder endpoint: {}'.format(endpoint))
    try:
        response = requests.post(endpoint,
                                 payload,
                                 verify=False,
                                 auth=(config.GEOCODE_BASIC_AUTH_USER, config.GEOCODE_BASIC_AUTH_PASS))
    except requests.ConnectionError as error:
        logging.warning('no response from the Geocoder API: {}'.format(error))
        return False, dict()

    if response.status_code != 200:
        logging.warning('response from the Geocoder API: {}'.format(response.text))
        return False, dict()

    data = response.json()
    logging.debug('VIPS API response: {}'.format(json.dumps(data)))
    args['geocoder_response'] = data
    return True, args


def add_geocode_response_to_message(**args) -> tuple:
    return True, args
