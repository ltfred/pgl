import sys

import click


def output(msg):
    """Print message"""
    click.edit(msg)
    sys.exit()
