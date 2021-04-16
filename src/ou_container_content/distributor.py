"""Distribute files from a source to a target location."""
import os
import shutil


def distribute(config: dict) -> None:
    """Distribute a full configuration.

    :param config: The configuration with the paths to copy
    :type config: dict
    """
    for path in config['paths']:
        distribute_path(path)


def distribute_path(path: dict) -> None:
    """Distribute a single path configuration.

    This will copy the file contents from source to target. Depending on the overwrite mode, existing files will or
    will not be overwritten.

    :param path: The path configuration to distribute
    :type path: dict
    """
    if os.path.exists(path['source']):
        for basepath, dirnames, filenames in os.walk(path['source']):
            for dirname in dirnames:
                targetpath = os.path.join(path['target'], os.path.join(basepath, dirname)[len(path['source']) + 1:])
                if not os.path.exists(targetpath):
                    os.makedirs(targetpath)
            for filename in filenames:
                targetpath = os.path.join(path['target'], os.path.join(basepath, filename)[len(path['source']) + 1:])
                exists = os.path.exists(targetpath)
                overwrite = path['overwrite'] == 'always'
                if not exists or overwrite:
                    shutil.copyfile(os.path.join(basepath, filename), targetpath)
