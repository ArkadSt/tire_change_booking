from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .views import get_workshops, get_tire_change_times, book_tire_change_time

# Tests are supposed to be run with the following config file in place: https://raw.githubusercontent.com/ArkadSt/tire_change_booking/refs/heads/main/backend/workshops.yaml
class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_workshops(self):
        url = reverse("get_workshops")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertIn("name", response.data[0])
        self.assertIn("address", response.data[0])
        self.assertIn("vehicle_types", response.data[0])

    def test_get_tire_change_times_no_workshop(self):
        url = reverse("get_tire_change_times")
        response = self.client.get(url, {"workshop": "london_tires", "from": "2025-01-01", "until": "2026-01-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertIn("time", response.data[0])
        self.assertIn("id", response.data[0])


    def test_get_tire_change_times_no_workshop(self):
        url = reverse("get_tire_change_times")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("'workshop' parameter expected", response.data["error"])

    def test_get_tire_change_times_invalid_workshop(self):
        url = reverse("get_tire_change_times")
        workshop_name = "invalid_workshop"
        response = self.client.get(url, {"workshop": workshop_name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("no workshop '{}' defined".format(workshop_name), response.data["error"])

    def test_book_tire_change_time_no_payload(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_book_tire_change_time_no_workshop(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"id": "69784c10-19d3-48c9-b14d-ad5651142c24"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_book_tire_change_time_invalid_workshop(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"workshop": "invalid_workshop", "id": "69784c10-19d3-48c9-b14d-ad5651142c24", "contact_info": "5555 5555"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_book_tire_change(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"workshop": "london_tires", "id": "69784c10-19d3-48c9-b14d-ad5651142c24", "contact_info": "5555 5555"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("time", response.data)

    def test_book_tire_change_invalid_id(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"workshop": "london_tires", "id": "5697845c10-in55valid-id-ad5651142c24", "contact_info": "5555 5555"})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("error", response.data)

    def test_book_tire_change_no_id(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"workshop": "london_tires", "contact_info": "5555 5555"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("'id' parameter expected", response.data["error"])

    def test_book_tire_change_time_no_contact_info(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"workshop": "london_tires", "id": "5697845c10-in55valid-id-ad5651142c24"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_book_tire_change_time_invalid_time(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"workshop": "london_tires", "time": "invalid_time"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_book_tire_change_time_invalid_vehicle_type(self):
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"workshop": "london_tires", "time": "10:00", "vehicle_type": "invalid_vehicle_type"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)