import asyncio
from kasa import Discover
from kasa import SmartPlug
import click


@click.command()
@click.option("--alias", prompt="Alias", help="The name of the device")
def query_state(alias):
    outlet = KasaOutlet()
    device = asyncio.run(outlet.discover_device(alias))
    state = asyncio.run(outlet.get_state(device))
    state_str = "on" if state else "off"
    print(f"{alias} is {state_str}")


class KasaOutlet:
    def __init__(self):
        pass

    async def discover_device(self, alias):
        devices = await Discover.discover(timeout=2)
        first_match = next(
            (k for (k, v) in devices.items() if alias == v.alias), None
        )
        if first_match is None:
            raise Exception(f"Failed to find device matching alias {alias}")
        else:
            return SmartPlug(first_match)

    async def get_state(self, device):
        await device.update()
        return device.is_on


if __name__ == "__main__":
    query_state()
