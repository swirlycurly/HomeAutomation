import atexit
import json
from googleapiclient.discovery import build
from projectId import get_project_id
from getCredentials import get_credentials


class Thermostat:
    def __init__(self):
        self.project_id = get_project_id()
        self.project_parent = f"enterprises/{self.project_id}"
        self.service = build(
            "smartdevicemanagement",
            version="v1",
            credentials=get_credentials(),
        )
        atexit.register(self.cleanup)

    def cleanup(self):
        self.service.close
        print("Thermostat service closed")

    def get_devices(self):
        devices_request = (
            self.service.enterprises()
            .devices()
            .list(parent=self.project_parent)
        )
        response = self.__execute(devices_request)
        return response["devices"]

    def get_temp(self, device_name):
        request = self.service.enterprises().devices().get(name=device_name)
        response = self.__execute(request)
        tempC = response["traits"]["sdm.devices.traits.Temperature"][
            "ambientTemperatureCelsius"
        ]
        return tempC

    def __execute(self, request, debug=False):
        response = request.execute()
        if debug:
            print(json.dumps(response, indent=2))
        return response
