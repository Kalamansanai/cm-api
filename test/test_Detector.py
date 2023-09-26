import domain.detector
from domain.detector import DetectorConfig, DetectorState
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
