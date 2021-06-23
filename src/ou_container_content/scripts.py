"""Run scripts."""
import math

from asyncio.subprocess import create_subprocess_exec

from .handlers import send_message


async def run_scripts(settings):
    """Run all scripts.

    :param config: The configuration with the scripts to run
    :type config: dict
    """
    send_message({
        'message': 'Running startup scripts...'
    })
    send_message({
        'component': 'scripts',
        'state': 'active',
        'progress': 0,
    })
    if 'scripts' in settings:
        for idx, script in enumerate(settings['scripts']):
            if 'cmd' in script:
                proc = await create_subprocess_exec(*script['cmd'].split(' '))
                await proc.wait()
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
