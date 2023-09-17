#!/usr/bin/env python

"""Simple script to acquire and log
temperature from nest thermostat
as well as the state of my whole house fan
"""
import asyncio
from thermostat import Thermostat
from database import Database
import kasaoutlet


def main():
    nestThermostatTable = "nestThermostat"
    wholeHouseFanTable = "wholeHouseFan"
    db = "homedata.db"
    fanAlias = "Whole House Fan"

    db = Database(db)
    db.create_data_table(nestThermostatTable)
    db.create_data_table(wholeHouseFanTable)

    nest = Thermostat()
    device = nest.get_devices()[0]
    device_name = device["name"]
    currentTemp = nest.get_temp(device_name)
    db.add_data(nestThermostatTable, currentTemp)

    fan = asyncio.run(kasaoutlet.discover_device(fanAlias))
    state = asyncio.run(kasaoutlet.get_state(fan))
    db.add_data(wholeHouseFanTable, state)


if __name__ == "__main__":
    main()
