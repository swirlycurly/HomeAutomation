#!/usr/bin/env python3

"""Simple script to acquire temperature from nest thermostat
"""

import os
import sys
import getCredentials


def main():
    credentials = getCredentials.getCredentials()


if __name__ == '__main__':
    main()
