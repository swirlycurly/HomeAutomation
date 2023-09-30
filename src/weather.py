import json
import logging
import requests
from requests.compat import urljoin


logger = logging.getLogger(__name__)
BASE = "https://api.weather.gov"
FLAGCOORDS = (35.1727, -111.6795)
TIMEOUT = 5


def get_forecast_reader(lat, long):
    try:
        headers = {"user-agent": "bcurl3ss@gmail.com"}
        url = urljoin(BASE, f"/points/{lat},{long}")
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        r.raise_for_status()
        fcastend = r.json()["properties"]["forecastHourly"]

        def get_forecast():
            r = requests.get(fcastend, headers=headers, timeout=TIMEOUT)
            return r.json()

        return get_forecast

    except Exception as e:
        logger.error("Failed to get weather forecast", e)
        raise e


if __name__ == "__main__":
    get_forecast = get_forecast_reader(*FLAGCOORDS)
    print(json.dumps(get_forecast(), indent=2))
