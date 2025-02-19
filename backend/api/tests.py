from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .views import get_workshops, get_tire_change_times, book_tire_change_time, CONFIG

# for running tests please use the following config file https://raw.githubusercontent.com/ArkadSt/tire_change_booking/refs/heads/main/backend/workshops.yaml
# and make sure that workshops are running https://github.com/Surmus/tire-change-workshop

class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.workshops = CONFIG.keys()
        self.date_format = "%Y-%m-%d"
        self.from_date = (datetime.now() - timedelta(days=365*100)).strftime(self.date_format)
        self.until_date = (datetime.now() + timedelta(days=365*100)).strftime(self.date_format)

    def get_first_available_id(self, workshop):
        url = reverse("get_tire_change_times")
        response = self.client.get(url, {"workshop": workshop, "from": self.from_date, "until": self.until_date})
        if response.status_code == status.HTTP_200_OK and len(response.data) > 0:
            return response.data[0]["id"]
        return None

    def test_get_workshops(self):
        url = reverse("get_workshops")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertIn("name", response.data[0])
        self.assertIn("address", response.data[0])
        self.assertIn("vehicle_types", response.data[0])

    def test_get_tire_change_times(self):
        for workshop in self.workshops:
            url = reverse("get_tire_change_times")
            response = self.client.get(url, {"workshop": workshop, "from": self.from_date, "until": self.until_date})
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
        for workshop in self.workshops:
            id = self.get_first_available_id(workshop)
            if not id:
                self.fail(f"No available times for {workshop}")
            url = reverse("book_tire_change_time")
            response = self.client.post(url, {"workshop": workshop, "id": id, "contact_info": "5555 5555"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("id", response.data)
            self.assertIn("time", response.data)

    def test_book_tire_change_invalid_id(self):
        for workshop in self.workshops:
            url = reverse("book_tire_change_time")
            response = self.client.post(url, {"workshop": workshop, "id": "invalid_id", "contact_info": "5555 5555"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("error", response.data)

    def test_book_tire_change_id_is_already_booked(self):
        workshop = "manchester_tires"
        id = self.get_first_available_id(workshop)
        if not id:
            self.fail(f"No available times for {workshop}")
        url = reverse("book_tire_change_time")
        response = self.client.post(url, {"workshop": workshop, "id": id, "contact_info": "5555 5555"})
        response = self.client.post(url, {"workshop": workshop, "id": id, "contact_info": "5555 5555"})
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("error", response.data)

    def test_book_tire_change_no_id(self):
        for workshop in self.workshops:
            url = reverse("book_tire_change_time")
            response = self.client.post(url, {"workshop": workshop, "contact_info": "5555 5555"})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("error", response.data)
            self.assertIn("'id' parameter expected", response.data["error"])

    def test_book_tire_change_time_no_contact_info(self):
        for workshop in self.workshops:
            id = self.get_first_available_id(workshop)
            if not id:
                self.fail(f"No available times for {workshop}")
            url = reverse("book_tire_change_time")
            response = self.client.post(url, {"workshop": workshop, "id": id})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("error", response.data)

