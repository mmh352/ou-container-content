"""Handle the startup/shutdown process."""
import tornado

from asyncio import sleep

from .handlers import send_message, completed
from .distributor import distribute
from .scripts import run_startup_scripts, run_shutdown_scripts
from .services import start_services, shutdown_services


async def startup(settings):
    """Run the startup process steps.

    :param config: The configuration
    :type config: dict
    """
    send_message('Container starting up...')
    await distribute(settings)
    await run_startup_scripts(settings)
    await start_services(settings)
    completed()
    await sleep(0.001)
    tornado.ioloop.IOLoop.current().stop()


async def shutdown(settings):
    """Run the shutdown process steps.

    :param config: The configuration
    :type config: dict
    """
    await shutdown_services(settings)
    await run_shutdown_scripts(settings)
    await sleep(0.001)
    tornado.ioloop.IOLoop.current().stop()
