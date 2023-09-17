#!/usr/bin/env python

"""Simple script to acquire and log
temperature from nest thermostat
as well as the state of my whole house fan
"""

import os
import sys
import time

from thermostat import Thermostat
from database import Database
from kasaoutlet import KasaOutlet


def main():
    nestThermostatTable = "nestThermostat"
    wholeHouseFanTable = "wholeHouseFan"
    nestdb = "nestdb.db"
    whf = "Whole House Fan"

    db = Database(nestdb)
    db.create_data_table(nestThermostatTable)
    db.create_data_table(wholeHouseFanTable)

    nest = Thermostat()
    device = nest.get_devices()[0]
    device_name = device["name"]
    currentTemp = nest.get_temp(device_name)
    db.add_data(nestThermostatTable, currentTemp)

    # outlet = KasaOutlet()
    # fan = outlet.discover_device(whf)
    # state = outlet.get_state(fan)
    # db.add_data(wholeHouseFanTable, state)


if __name__ == "__main__":
    main()
