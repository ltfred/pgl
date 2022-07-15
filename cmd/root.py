import click

from cmd.pgl import PGL


@click.group()
def pgl():
    pass


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
