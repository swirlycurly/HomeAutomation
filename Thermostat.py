from googleapiclient.discovery import build
from projectId import get_project_id
from getCredentials import get_credentials
import atexit
import json


class Thermostat:
    def __init__(self):
        self.project_id = get_project_id() 
        self.project_parent = f"enterprises/{self.project_id}"
        self.service = build('smartdevicemanagement', version='v1',
                             credentials=get_credentials())
        atexit.register(self.cleanup)

    def cleanup(self):
        self.service.close
        print('Thermostat service closed')

    def get_devices(self):
        devices_request = self.service.enterprises().devices()\
            .list(parent=self.project_parent)
        response = self.__execute(devices_request)
        return response['devices']

    def get_temp(self):
        device = self.get_devices()[0]
        deviceName = device["name"]  # .split('/')[-1]
        print(deviceName)
        request = self.service.enterprises().devices().get(name=deviceName)
        response = self.__execute(request)
        tempC = response["traits"]["sdm.devices.traits.Temperature"]
        return tempC

    def __execute(self, request):
        response = request.execute()

        print(json.dumps(response, indent=2))
        return response
