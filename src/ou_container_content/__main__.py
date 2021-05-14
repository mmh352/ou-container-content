"""The OU Container Content distribution application commandline interface."""
import click
import tornado.ioloop
import tornado.web

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from .handlers import WebsocketHandler, StaticHandler
from .process import process
from .validator import validate_settings


def make_app():
    """Build the tornado web application."""
    return tornado.web.Application([
        (r".*websocket", WebsocketHandler),
        (r".*build/(.*)", StaticHandler, {'base_path': 'build/'}),
        (r".*(global.css)", StaticHandler, {'base_path': ''}),
        (r".*(ou-favicon-[0-9]+.png)", StaticHandler, {'base_path': ''}),
        (r".*", StaticHandler, {'base_path': 'index.html'}),
    ])


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
        app = make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().add_callback(process, settings)
        tornado.ioloop.IOLoop.current().start()
    else:
        click.echo(click.style('There are errors in your configuration settings:', fg='red'), err=True)
        click.echo(err=True)

        for error in settings:
            click.echo(error, err=True)

        raise click.Abort()


if __name__ == '__main__':
    main()
