from datetime import datetime, timezone

import requests
from abc import ABC, abstractmethod


def map_fields(data, mapping, reverse=False):
    """
    Maps fields based on configuration.
    - `reverse=True` : Map workshop's response fields to standard format.
    - `reverse=False` (default): Map standard format back to workshop-specific fields.
    """
    if reverse:
        # Reverse field mapping: Convert standard format to workshop's format
        return {k: data[v] for k, v in mapping.items() if v in data}
    else:
        # Standard field mapping: Convert workshop's format to standard format
        return {v: data[k] for k, v in mapping.items() if k in data}

class BaseAdapter(ABC):
    """Abstract base class for workshop API integrations."""

    def __init__(self, workshop_id, workshop_config):

        self.base_url = workshop_config["base_url"]
        self.endpoints = workshop_config["endpoints"]
        self.field_mappings = workshop_config["field_mappings"]
        self.param_mappings = workshop_config["param_mappings"]
        self.vehicle_types = workshop_config["vehicle_types"]
        self.workshop_id = workshop_id
        self.workshop_name = workshop_config["name"]
        self.workshop_address = workshop_config["address"]

    @abstractmethod
    def fetch_available_slots(self, params):
        pass

    @abstractmethod
    def book_appointment(self, payload):
        pass

    def prepare_url(self, payload):
        """
        Injects ID into booking url
        """
        return self.base_url + self.endpoints["book_appointment"]["endpoint"].format(id=payload["booking_id"])

    def get_available_slots_response(self, params):
        url = self.base_url + self.endpoints["available_slots"]["endpoint"]
        return requests.request(self.endpoints["available_slots"]["method"], url, params=map_fields(params, self.param_mappings["available_slots"]))

    def add_information_to_slot(self, entry):
        entry["workshop"] = {
            "id": self.workshop_id,
            "name": self.workshop_name,
            "address": self.workshop_address,
            "vehicle_types": self.vehicle_types,
        }

    def prepare_available_slots(self, payload, params):
        response = []
        for entry in payload:
            entry = map_fields(entry, self.field_mappings, reverse=True)
            if not self.param_mappings["available_slots"]["from"] and datetime.fromisoformat(entry["time"]) < datetime.fromisoformat(params["from"]).replace(tzinfo=timezone.utc):
                continue
            if not self.param_mappings["available_slots"]["until"] and datetime.fromisoformat(entry["time"]) > datetime.fromisoformat(params["until"]).replace(tzinfo=timezone.utc):
                continue

            try:
                if not entry["available"]:
                    continue
                entry.pop("available")
            except KeyError:
                pass

            self.add_information_to_slot(entry)
            response.append(entry)
        return response