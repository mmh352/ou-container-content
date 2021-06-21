"""Start and stop services."""
import math

from subprocess import run

from .handlers import send_message


async def start_services(settings):
    """Start all services.

    :param config: The configuration with the services to start
    :type config: dict
    """
    if 'services' in settings:
        for idx, service in enumerate(settings['services']):
            run(['service', service, 'start'])
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
