from requests import HTTPError

from api.adapters.base_adapter import BaseAdapter, map_fields
import requests
import xml.etree.ElementTree as ET
from rest_framework.response import Response

def xml_to_dict(root : ET.Element):
    dic = {}
    for entry in root:
        dic[entry.tag] = entry.text
    return dic


class XmlAdapter(BaseAdapter):
    def fetch_available_slots(self, params):
        response = self.get_available_slots_response(params)
        try:
            response.raise_for_status()
            payload = []
            for time in ET.fromstring(response.text):
                payload.append(xml_to_dict(time))

            payload = self.prepare_available_slots(payload, params)
            return Response(payload, status=response.status_code)
        except HTTPError:
            payload = map_fields(xml_to_dict(response.text), self.field_mappings, reverse=True)
            return Response(payload, status=response.status_code)


    def book_appointment(self, payload):

        url = self.prepare_url(payload)
        # Convert to workshop-specific format
        mapped_slot_data = map_fields(payload, self.field_mappings)

        request = ET.Element("xml_request_tag")
        for key, value in mapped_slot_data.items():
            ET.SubElement(request, key).text=value
        headers = {'Content-Type': 'application/xml'}
        response = requests.request(self.endpoints["book_appointment"]["method"], url, data=ET.tostring(request), headers=headers)

        payload = {}
        for entry in ET.fromstring(response.text):
            payload[entry.tag] = entry.text

        #response.raise_for_status()
        return Response(map_fields(payload, self.field_mappings, reverse=True), status=response.status_code)