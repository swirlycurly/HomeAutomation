import logging
import requests
from requests.compat import urljoin
import json


logger = logging.getLogger(__name__)
base = "https://api.weather.gov"
flagCoords = (35.1727, -111.6795)
timeout = 5


def get_forecast_reader(lat, long):
    try:
        headers = {"user-agent": "bcurl3ss@gmail.com"}
        url = urljoin(base, f"/points/{lat},{long}")
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        fcastend = r.json()["properties"]["forecastHourly"]

        def get_forecast():
            r = requests.get(fcastend, headers=headers, timeout=timeout)
            return r.json()

        return get_forecast

    except Exception as e:
        logger.error("Failed to get weather forecast", e)
        raise e


if __name__ == "__main__":
    get_forecast = get_forecast_reader(*flagCoords)
    print(json.dumps(get_forecast(), indent=2))
