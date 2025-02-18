from api.adapters.json_adapter import JsonAdapter
from api.adapters.xml_adapter import XmlAdapter

def create_adapter(workshop_id, workshop_config):
    match workshop_config["request_format"]:
        case "json":
            return JsonAdapter(workshop_id, workshop_config)
        case "xml":
            return XmlAdapter(workshop_id, workshop_config)
        case _:
            raise ValueError("Unsupported request format {}".format(workshop_config["request_format"]))