#!/usr/bin/env python3

"""Simple script to acquire temperature from nest thermostat
"""

import os
import sys
from projectId import get_project_id
from Thermostat import Thermostat
import time

def main():
    nest = Thermostat()
    while True:
        print(nest.get_temp())
        time.sleep(5)


if __name__ == '__main__':
    main()
