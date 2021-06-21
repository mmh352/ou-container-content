"""Handle the startup process."""
import tornado

from asyncio import sleep

from .handlers import send_message, completed
from .distributor import distribute
from .scripts import run_scripts


async def process(settings):
    """Run the startup process steps.

    :param config: The configuration
    :type config: dict
    """
    send_message('Container starting up...')
    await distribute(settings)
    await run_scripts(settings)
    send_message({
        'component': 'services',
        'state': 'complete',
        'progress': 100,
    })
    completed()
    await sleep(0.001)
    tornado.ioloop.IOLoop.current().stop()
