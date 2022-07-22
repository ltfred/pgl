from cmd.pgl import PGL

import cmd
import click


@click.group()
@click.version_option(cmd.__version__, prog_name="pgl")
def pgl():
    """Pgl is a cli tool, include some shortcut for gitlab"""


@pgl.command()
def config():
    """Edit config file"""
    PGL().config()


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
