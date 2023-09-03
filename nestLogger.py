#!/usr/bin/env python3

"""Simple script to acquire temperature from nest thermostat
"""

import os
import sys
import time

from Thermostat import Thermostat


def main():
    nest = Thermostat()
    device = nest.get_devices()[0]
    device_name = device["name"]  # .split('/')[-1]

    while True:
        print(nest.get_temp(device_name))
        time.sleep(5)


if __name__ == '__main__':
    main()
