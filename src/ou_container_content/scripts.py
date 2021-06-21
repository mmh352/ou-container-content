"""Run scripts."""
import math

from subprocess import run

from .handlers import send_message


async def run_scripts(settings):
    """Run all scripts.

    :param config: The configuration with the scripts to run
    :type config: dict
    """
    if 'scripts' in settings:
        for idx, script in enumerate(settings['scripts']):
            if 'cmd' in script:
                run(script['cmd'].split(' '))
            send_message({
                'component': 'scripts',
                'state': 'active',
                'progress': math.floor(100 / len(settings['scripts']) * idx),
            })
    send_message({
        'component': 'scripts',
        'state': 'complete',
        'progress': 100,
    })