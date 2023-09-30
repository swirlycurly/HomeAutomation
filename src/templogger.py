#!/usr/bin/env python

"""Simple script to acquire and log
home automation data
"""
import os
import time
from datetime import datetime
import logging
from logging.handlers import SysLogHandler
import asyncio
import click
import schedule
from pythonjsonlogger import jsonlogger
from thermostat import Thermostat
from database import TimeSeriesDb
import kasaoutlet


@click.command()
@click.option("-i", "--interval", default=1)
def monitor(interval):
    logger = _log_setup()
    nest_thermostat_name = "nestThermostat"
    fan_table_name = "wholeHouseFan"
    dbname = "homedata.db"
    fan_alias = "Whole House Fan"

    try:
        logger.debug("Initializing Home Automation Logger Script")

        db = TimeSeriesDb(dbname)
        db.create_table(
            nest_thermostat_name,
            "temperatureC",
            "hvacStatus",
            "humidity",
            "setpointC",
        )
        db.create_table(fan_table_name, "value")
    except Exception as e:
        logger.error("Failed to initialize house monitoring", e)
        return

    def update():
        try:
            nest = Thermostat()
            device = nest.get_devices()[0]
            device_name = device["name"]
            traits = nest.get_traits(device_name)
            db.add_data(
                nest_thermostat_name,
                Thermostat.extract_temp(traits),
                Thermostat.extract_hvac_status(traits),
                Thermostat.extract_humidity(traits),
                Thermostat.extract_setpoint(traits),
            )

            fan = asyncio.run(kasaoutlet.discover_device(fan_alias))
            state = asyncio.run(kasaoutlet.get_state(fan))
            db.add_data(fan_table_name, state)
        except Exception as e:
            logger.error("Failed to update value", e)

    schedule.every(interval).minutes.do(update)
    while True:
        schedule.run_pending()
        time.sleep(5)


def _log_setup():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = SysLogHandler(
        facility=SysLogHandler.LOG_DAEMON, address="/dev/log"
    )
    formatter = CustomJsonFormatter("%(level)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        log_record["app_name"] = os.path.basename(__file__)


if __name__ == "__main__":
    monitor()
