"""The OU Container Content distribution application commandline interface."""
import click

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .distributor import distribute
from .validator import validate_settings


@click.command()
@click.option('-c', '--config',
              type=click.File(),
              default='/etc/module-content/config.yaml',
              help='The configuration file to use')
def main(config: click.File):
    """OU Container Content distribution."""
    settings = load(config, Loader=Loader)
    settings = validate_settings(settings)
    if isinstance(settings, dict):
        distribute(settings)
    else:
        click.echo(click.style('There are errors in your configuration settings:', fg='red'), err=True)
        click.echo(err=True)

        for error in settings:
            click.echo(error, err=True)

        raise click.Abort()


if __name__ == '__main__':
    main()
