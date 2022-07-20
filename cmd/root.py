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
def browser():
    """Open project in browser"""
    PGL().browser()
