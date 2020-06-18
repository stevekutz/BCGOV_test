from python.common.helper import load_json_into_dict


def test_get_queue_config_ingestor():
    queues_data = load_json_into_dict('python/ingestor/parameters.json')
    assert type(queues_data) is dict
    assert "ETK" in queues_data
    assert "IRP" in queues_data
