# -*- coding: utf-8 -*-

import click
from models import initialisedb


@click.group()
def cli():
    pass


@cli.command(name='initialisedb')
def initialisedb_command():
    initialisedb()


if __name__ == '__main__':
    cli()
