from cmd.pgl import PGL

import click


@click.group()
def pgl():
    """Root cmd"""


@pgl.command()
def config():
    """Edit config file"""
    PGL().config()


@pgl.command()
def version():
    """Display version for pgl"""
    PGL().version()


@pgl.command()
def sync():
    """Sync projects"""
    PGL().sync()


@pgl.command()
def clone():
    """Clone project"""
    PGL().clone()


@pgl.command()
@click.option("-p", "pipeline", is_flag=True, help="Open project pipelines in web browser")
def browser(pipeline):
    """Open project in web browser"""
    PGL().browser(pipeline)
