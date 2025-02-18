from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .adapters import adapter_factory
from .parsers import yaml_loader
from functools import wraps

# Create your views here.

CONFIG: dict = yaml_loader.load_workshops()

@api_view(['GET'])
def get_workshops(request: Request) -> Response:
    workshops = CONFIG.keys()
    response = []
    for workshop in workshops:
        config = CONFIG[workshop]
        response.append({"id": workshop, "name": config["name"], "address": config["address"],"vehicle_types": config["vehicle_types"]})
    return Response(response)

def handle_workshop_errors(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        workshop = request.query_params.get('workshop') or request.data.get('workshop')
        if not workshop:
            return Response({"error": "'workshop' parameter expected"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            config = CONFIG[workshop]
        except KeyError as e:
            return Response({"error": "no workshop {} defined".format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        return view_func(request, workshop, config, *args, **kwargs)

    return _wrapped_view

@api_view(['GET'])
@handle_workshop_errors
def get_tire_change_times(request, workshop_id, config):
    return adapter_factory.create_adapter(workshop_id, config).fetch_available_slots(request.query_params)

@api_view(['POST'])
@handle_workshop_errors
def book_tire_change_time(request, workshop_id, config):
    if not 'id' in request.data:
        return Response({"error": "'id' parameter expected"}, status=status.HTTP_400_BAD_REQUEST)
    return adapter_factory.create_adapter(workshop_id, config).book_appointment(request.data)
