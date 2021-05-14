"""Distribute files from a source to a target location."""
import math
import os
import shutil

from asyncio import sleep

from .handlers import send_message


async def distribute(config: dict) -> None:
    """Distribute a full configuration.

    :param config: The configuration with the paths to copy
    :type config: dict
    """
    send_message({
        'message': 'Determining files to update. This can take a bit. Please wait...'
    })
    send_message({
        'component': 'files',
        'state': 'active',
        'progress': 0,
    })
    updates = []
    for idx, path in enumerate(config['paths']):
        send_message({
            'component': 'files',
            'state': 'active',
            'progress': math.floor(100 / len(config['paths']) * idx),
        })
        updates.extend(await determine_updates(path))
        await sleep(0.1)
    send_message({
        'message': 'Updating files...'
    })
    for idx, update in enumerate(updates):
        if update[0] == 'dir':
            os.makedirs(update[1], exist_ok=True)
        elif update[0] == 'file':
            dirname = os.path.dirname(update[2])
            os.makedirs(dirname, exist_ok=True)
            shutil.copyfile(update[1], update[2])
        if idx % 10 == 0:
            send_message({
                'component': 'files',
                'state': 'active',
                'progress': math.floor(100 / len(updates) * idx),
            })
            await sleep(0.001)
    send_message({
        'message': 'Your files have been copied.'
    })
    send_message({
        'component': 'files',
        'state': 'complete',
        'progress': 100,
    })


async def determine_updates(path: dict) -> list:
    """Distribute a single path configuration.

    This will copy the file contents from source to target. Depending on the overwrite mode, existing files will or
    will not be overwritten.

    :param path: The path configuration to distribute
    :type path: dict
    """
    updates = []
    if os.path.exists(path['source']):
        for basepath, dirnames, filenames in os.walk(path['source']):
            for dirname in dirnames:
                targetpath = os.path.join(path['target'], os.path.join(basepath, dirname)[len(path['source']) + 1:])
                if not os.path.exists(targetpath):
                    updates.append(('dir', targetpath))
            for filename in filenames:
                targetpath = os.path.join(path['target'], os.path.join(basepath, filename)[len(path['source']) + 1:])
                exists = os.path.exists(targetpath)
                overwrite = path['overwrite'] == 'always'
                if not exists or overwrite:
                    updates.append(('file', os.path.join(basepath, filename), targetpath))
    return updates
