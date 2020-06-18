import logging
from python.common.helper import load_json_into_dict
from cerberus import Validator as Cerberus


class Validate:

    def __init__(self, config):
        self.schemas = load_json_into_dict(config.SCHEMA_PATH + config.SCHEMA_FILENAME)
        logging.basicConfig(level=config.LOG_LEVEL)

    def validate(self, message: dict) -> dict:
        """
            The validate methods looks up a schema with the same event_type
            in the schemas json file, and uses the validation rules described
            in the file to determine if the message is valid.  This method
            returns a dictionary with the status of the validation and, if not
            successful, an error message.
        :param message:
        :return: dictionary
        """

        cerberus_errors = []

        # check that message is a dictionary
        if not isinstance(message, dict):
            error_message = 'the message does not decode into a dictionary object'
            logging.info(error_message)
            return {'isSuccess': False, 'description': error_message}

        # loop through each schema, stop on the first to pass validation
        # return the validation error message from the schema that best fits
        for schema in self.schemas:
            cerberus = Cerberus(schema['cerberus_rules'])
            cerberus.allow_unknown = schema['allow_unknown']
            if cerberus.validate(message):
                logging.info(' - message passed validation for type: ' + schema['name'])
                return {'isSuccess': True, 'description': ''}
            else:
                cerberus_errors.append(cerberus.errors)

        logging.info(' - message failed validation validation')
        return {'isSuccess': False, 'description': self.get_best_error(cerberus_errors)}

    @staticmethod
    def get_best_error(errors: list):
        # TODO - develop an algorithm that returns the error messages
        #  from the schema with best match.
        return errors.pop(0)
