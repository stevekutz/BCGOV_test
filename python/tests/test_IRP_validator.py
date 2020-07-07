import json
from python.validator.config import Config as ValidationConfig
from python.validator.validator import Validate
from python.common.helper import load_json_into_dict


# To override the config class for testing
class Config(ValidationConfig):
    SCHEMA_FILENAME = 'form_schemas.json'
    

class TestIrpValidator:

    def test_sample_irp_form_submission_passes_validation(self):
        sample_data = load_json_into_dict('python/tests/sample_data/irp_form_submission.json')
        assert type(sample_data) is dict
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is True

    def test_sample_irp_form_submission_fails_validation_with_missing_section(self):
        sample_data = load_json_into_dict('python/tests/sample_data/irp_form_submission.json')
        del sample_data['form']['section-irp-information']
        validate_class = Validate(Config())
        assert validate_class.validate(sample_data)['isSuccess'] is False
        assert 'section-irp-information' in validate_class.validate(sample_data)['description']['form'][0]
