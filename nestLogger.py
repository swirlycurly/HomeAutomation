#!/usr/bin/env python

"""Simple script to acquire and log
temperature from nest thermostat
"""

import os
import sys
import time

from Thermostat import Thermostat
from sqliteDatabase import sqliteDatabase


def main():
    nestThermostatTable = "nestThermostat"
    nestdb = "nestdb.db"
    nest = Thermostat()
    device = nest.get_devices()[0]
    device_name = device["name"]  # .split('/')[-1]
    db = sqliteDatabase(nestdb)
    db.create_data_table(nestThermostatTable)

    currentTemp = nest.get_temp(device_name)
    db.add_data(nestThermostatTable, currentTemp)


if __name__ == "__main__":
    main()
