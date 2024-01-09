import datetime
from api.diagrams import monthly_sums_bar
def test_monthly_stat_calculate_with_sortingMultipleTypes():
   input = [
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "water",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
         "value": 5
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "water",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 20),
         "value": 10
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "gas",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
         "value": 10
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "gas",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 20),
         "value": 20
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "electricity",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
         "value": 5
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "electricity",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 20),
         "value": 30
      }
   ]
   response = monthly_sums_bar.monthly_stat(input)
   assert response[0]["water"] == 5
   assert response[0]["gas"] == 10
   assert response[0]["electricity"] == 25
def test_monthly_stat_calculate_with_sortingMultipleTypes_andMultipleMonths():
   input = [
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "water",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
         "value": 5
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "water",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 20),
         "value": 10
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "water",
         "timestamp": datetime.datetime(2023, 7, 24, 10, 10),
         "value": 12
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "gas",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
         "value": 10
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "gas",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 20),
         "value": 20
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "gas",
         "timestamp": datetime.datetime(2023, 7, 24, 10, 10),
         "value": 23
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "electricity",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
         "value": 5
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "electricity",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 20),
         "value": 30
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "electricity",
         "timestamp": datetime.datetime(2023, 7, 24, 10, 10),
         "value": 8
      }
   ]
   response = monthly_sums_bar.monthly_stat(input)
   assert response[0]["water"] == 5
   assert response[0]["gas"] == 10
   assert response[0]["electricity"] == 25
   assert response[1]["water"] == 12
   assert response[1]["gas"] == 23
   assert response[1]["electricity"] == 8
def test_monthly_stat_calculate_withoutTypeParameter():
   input = [
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "gas",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
         "value": 10
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "gas",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 20),
         "value": 20
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "electricity",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
         "value": 5
      },
      {
         "location_id": 1,
         "detector_id": 1,
         "type": "electricity",
         "timestamp": datetime.datetime(2023, 6, 24, 10, 20),
         "value": 30
      }
   ]
   response = monthly_sums_bar.monthly_stat(input)
   assert response[0]["water"] == 0
   assert response[0]["gas"] == 10
   assert response[0]["electricity"] == 25
