import sys

import click


def output(msg):
    click.edit(msg)
    sys.exit()
