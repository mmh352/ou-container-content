"""Start and stop services."""
import math

from asyncio.subprocess import create_subprocess_exec

from .handlers import send_message


async def start_services(settings):
    """Start all services.

    :param config: The configuration with the services to start
    :type config: dict
    """
    if 'services' in settings:
        for idx, service in enumerate(settings['services']):
            proc = create_subprocess_exec(['sudo', 'service', service, 'start'])
            await proc.wait()
            send_message({
                'component': 'services',
                'state': 'active',
                'progress': math.floor(100 / len(settings['scripts']) * idx),
            })
    send_message({
        'component': 'services',
        'state': 'complete',
        'progress': 100,
    })
