# -*- coding: utf-8 -*-
import json

import click
import time

from druid_cli.druid import DruidMixedAPI
from druid_cli.types import LOCATION

INDENT = 3


@click.group()
@click.option('--overlord', default=None, type=LOCATION,
              envvar="DRUID_OVERLORD",
              help="Hostname and port of overlord node")
@click.option('--coordinator', default=None, type=LOCATION,
              envvar="DRUID_COORDINATOR",
              help="Hostname and port of coordinator node")
@click.option('--broker', default=None, type=LOCATION,
              envvar="DRUID_BROKER",
              help="Hostname and port of broker node")
@click.pass_context
def cli(ctx, overlord, coordinator, broker):
    ctx.obj = {
        'api': DruidMixedAPI(overlord, coordinator, broker)
    }


@cli.group(help="note: requires druid broker node")
def datasource():
    pass


@datasource.command(name="list")
@click.pass_context
def list_(ctx):
    api = ctx.obj['api']
    click.echo(json.dumps(api.get_datasources(), indent=INDENT))


@datasource.command()
@click.pass_context
@click.argument('datasources', nargs=-1)
def details(ctx, datasources):
    api = ctx.obj['api']
    available_datasources = api.get_datasources()

    output = {
        datasource_id: api.get_datasource(datasource_id)
        for datasource_id
        in available_datasources
        if datasource_id in datasources or not datasources
    }
    click.echo(json.dumps(output, indent=INDENT))


@cli.group(help="note: requires druid coordinator node")
def server():
    pass


@server.command(name="list", help="print list of servers")
@click.pass_context
def list_(ctx):
    api = ctx.obj['api']
    click.echo(json.dumps(api.get_servers(), indent=INDENT))


@server.command(help="print details of each server")
@click.pass_context
@click.argument('servers', nargs=-1)
def details(ctx, servers):
    api = ctx.obj['api']
    available_servers = api.get_servers()

    output = {
        server_id: api.get_server(server_id)
        for server_id
        in available_servers
        if server_id in servers or not servers
    }
    click.echo(json.dumps(output, indent=INDENT))


@server.command()
@click.pass_context
@click.argument('servers', nargs=-1)
def segments(ctx, servers):
    api = ctx.obj['api']
    available_servers = api.get_servers()

    output = {
        server_id: api.get_server_segments(server_id)
        for server_id
        in available_servers
        if server_id in servers or not servers
    }
    click.echo(json.dumps(output, indent=INDENT))


@server.command()
@click.pass_context
@click.option('--timeout', type=click.INT,  default=None, help="wait timeout in seconds",)
@click.argument('servers', nargs=-1)
def waitempty(ctx, timeout, servers):
    api = ctx.obj['api']
    available_servers = api.get_servers()

    start = time.time()

    while time.time() - start < timeout or not timeout:
        server_segments = [
            api.get_server_segments(server_id)
            for server_id
            in available_servers
            if server_id in servers or not servers
        ]
        if not any(server_segments):
            break

        time.sleep(1)
    else:
        click.echo('Wait timeout!')
        exit(1)


@cli.group(help="note: requires druid coordinator node")
def rule():
    pass


@rule.command(name='list', help="print list of all rules")
@click.pass_context
def list_(ctx):
    api = ctx.obj['api']
    click.echo(json.dumps(api.get_rules(), indent=INDENT))
