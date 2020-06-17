from python.common.helper import load_json_into_dict
# from python.ingestor.ingest import application
import pytest

#
# @pytest.fixture()
# def app():
#     return application.run()


def test_home_page(class_mocker):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    
    m = class_mocker('python.common.RabbitMQ')
    assert str(type(m)) == "RabbitMQ"

    # response = client.post('/v1/publish/event')
    # assert response.status_code == 200


def test_get_queue_config_ingestor():
    queues_data = load_json_into_dict('python/ingestor/parameters.json')
    assert type(queues_data) is dict
    assert "ETK" in queues_data['queues']
