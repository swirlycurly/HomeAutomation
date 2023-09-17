#!usr/bin/env python
import atexit
import json
from googleapiclient.discovery import build
from projectid import get_project_id
from credentials import get_credentials


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

    def get_devices(self, debug=False):
        devices_request = (
            self.service.enterprises()
            .devices()
            .list(parent=self.project_parent)
        )
        response = self._execute(devices_request, debug)
        return response["devices"]

    def get_temp(self, device_name):
        request = self.service.enterprises().devices().get(name=device_name)
        response = self._execute(request)
        tempC = response["traits"]["sdm.devices.traits.Temperature"][
            "ambientTemperatureCelsius"
        ]
        return tempC

    def _execute(self, request, debug=False):
        response = request.execute()
        if debug:
            print(json.dumps(response, indent=2))
        if response is {}:
            print(
                "Empty response. Check that you have given access to the devices"
            )
            raise Exception("Empty Response from request")
        return response