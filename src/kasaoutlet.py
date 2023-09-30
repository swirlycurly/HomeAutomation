import logging
import asyncio
from kasa import Discover
from kasa import SmartPlug
import click


logger = logging.getLogger(__name__)


@click.command()
@click.option("--alias", prompt="Alias", help="The name of the device")
def query_state(alias):
    device = asyncio.run(discover_device(alias))
    state = asyncio.run(get_state(device))
    state_str = "on" if state else "off"
    print(f"{alias} is {state_str}")


async def discover_device(alias):
    devices = await Discover.discover(timeout=2)
    logger.debug("Discovered Kasa devices: %s", devices)
    first_match = next(
        (k for (k, v) in devices.items() if alias == v.alias), None
    )
    if first_match is None:
        raise Exception(f"Failed to find device matching alias {alias}")
    else:
        logger.info("Kasa device matching alias %s is %s", alias, first_match)
        return SmartPlug(first_match)


async def get_state(device):
    await device.update()
    return device.is_on
