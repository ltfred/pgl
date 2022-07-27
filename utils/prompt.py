import click


def output(msg: str, color: str = ""):
    """Output information to the terminal"""
    if color == "":
        click.echo(msg)
    else:
        click.secho(msg, fg=color)
