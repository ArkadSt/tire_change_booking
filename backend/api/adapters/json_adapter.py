from requests import HTTPError

from api.adapters.base_adapter import BaseAdapter, map_fields
import requests
from rest_framework.response import Response

class JsonAdapter(BaseAdapter):
    def fetch_available_slots(self, params):
        response = self.get_available_slots_response(params)
        try:
            response.raise_for_status()
            payload = self.prepare_available_slots(response.json(), params)
            return Response(payload, status=response.status_code)
        except HTTPError:
            return Response(map_fields(response.json(), self.field_mappings, reverse=True), status=response.status_code)

    def book_appointment(self, payload):

        url = self.prepare_url(payload)
        # Convert to workshop-specific format
        mapped_slot_data = map_fields(payload, self.field_mappings)

        response = requests.request(self.endpoints["book_appointment"]["method"], url, json=mapped_slot_data)

        #response.raise_for_status()
        return Response(map_fields(response.json(), self.field_mappings, reverse=True), status=response.status_code)