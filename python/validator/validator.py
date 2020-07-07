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
            cerberus_errors.append([cerberus.errors])

        logging.info(' - message failed validation validation')
        return {'isSuccess': False, 'description': self.get_best_error(cerberus_errors)}

    @staticmethod
    def get_best_error(list_of_errors: list):
        """
        The validation process loops through a list of schemas stopping when
        it finds a match.  If it doesn't find a match, we don't know which
        schema was the closest match. This method returns the schema with the
        fewest errors -- assuming that's the schema that's most relevant.
        :param list_of_errors:
        :return:
        """
        relevant_errors = []
        first_loop = True
        for errors in list_of_errors:
            if first_loop:
                relevant_errors = errors
                first_loop = False
            if len(errors) < len(relevant_errors):
                relevant_errors = errors
        return relevant_errors[0]
