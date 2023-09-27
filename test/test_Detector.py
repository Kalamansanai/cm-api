import pytest
import domain.detector
from domain.detector import DetectorConfig, DetectorState, Detector
@pytest.fixture
def testDetector_json():
    return {
        "_id": 1,
        "location_id": 2,
        "detector_id": "3",
        "detector_name": "test",
        "type": "test",
        "state": "init",
        "detector_config": {"char_num": 544}
    }
def test_detector_get_db(testDetector_json):
    test_Detector = Detector(testDetector_json)
    response = test_Detector.get_db()
    assert response["_id"] == 1
    assert response["location_id"] == 2
    assert response["detector_id"] == "3"
    assert response["detector_name"] == "test"
    assert response["type"] == "test"
    assert response["state"] == "DetectorState.INIT"
    assert response["detector_config"]["char_num"] == 544
def test_get_json(testDetector_json):
    test_Detector = Detector(testDetector_json)
    response = test_Detector.get_json()
    assert response["id"] == "1"
    assert response["location_id"] == "2"
    assert response["detector_id"] == "3"
    assert response["detector_name"] == "test"
    assert response["type"] == "test"
    assert response["state"] == "DetectorState.INIT"
    assert response["detector_config"]["char_num"] == 544
def test_create_detector_for_mongo():
    response = domain.detector.create_detector_for_mongo(
        "1",
        "2",
        "test",
        544,
        5,
        "test"
    )
    assert response["location_id"] == "2"
    assert response["detector_id"] == "1"
    assert response["detector_name"] == "test"
    assert response["type"] == "test"
    assert response["detector_config"]["char_num"] == 544
    assert response["detector_config"]["coma_position"] == 5
def test_detector_valid():
    id_good = "18db1559-982d-4ede-92b6-9b21e05acdc2"
    id_fake = "test"
    response_true = domain.detector.detector_valid(id_good)
    response_false = domain.detector.detector_valid(id_fake)
    assert response_true is True
    assert response_false is False
def test_DetectorConfig_get_json():
    test_config = DetectorConfig({"char_num": 544})
    response = test_config.get_json()
    assert response["char_num"] == 544
    assert response["coma_position"] == ""
    assert response["delay"] == 0
def test_map_state():
    test_init = "init"
    test_sleep = "sleep"
    test_fake = "test"
    assert domain.detector.map_state(test_init) == DetectorState.INIT
    assert domain.detector.map_state(test_sleep) == DetectorState.SLEEP
    assert domain.detector.map_state(test_fake) == DetectorState.INIT
