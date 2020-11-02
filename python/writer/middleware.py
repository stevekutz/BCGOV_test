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
    endpoint = 'http://' + config.GEOCODER_API_URI + '/address'
    payload = args.get('payload')
    logging.info('Geocoder endpoint: {}'.format(endpoint))
    try:
        response = requests.post(endpoint,
                                 json=payload,
                                 verify=False,
                                 auth=(config.GEOCODE_BASIC_AUTH_USER, config.GEOCODE_BASIC_AUTH_PASS))
    except requests.ConnectionError as error:
        logging.warning('no response from the Geocoder API: {}'.format(error))
        return False, args

    if response.status_code != 200:
        error_message_string = response.text
        logging.warning('response from the Geocoder API: {}'.format(error_message_string))
        args['error_message_string'] = error_message_string
        return False, args

    data = response.json()
    logging.info('VIPS API response: {}'.format(json.dumps(data)))
    args['geocoder_response'] = data
    return True, args


def transform_geocoder_response(**args) -> tuple:
    """
    Transform the response from the Geocoder API into a format
    required by the BI geolocation table
    """
    geocoder = args.get('geocoder_response')
    args['geolocation'] = dict({
        "business_program": "BI",
        "business_type": "ETK",
        "business_id": "???",
        "long": geocoder['data_bc']['lon'],
        "lat": geocoder['data_bc']['lat'],
        # "precision": None,
        "requested_address": geocoder['address_raw'],
        "submitted_address": geocoder['address_clean'],
        "databc_long": geocoder['data_bc']['lon'],
        "databc_lat": geocoder['data_bc']['lat'],
        "databc_score": geocoder['data_bc']['score'],
        # "databc_precision": None
    })
    return True, args


def add_geolocation_data_to_message(**args) -> tuple:
    message = args.get('message')
    geolocation = args.get('geolocation')
    event_type = message['event_type']
    message[event_type]['geolocation'] = geolocation
    args['message'] = message
    logging.info("added geolocation data to the message")
    return True, args
