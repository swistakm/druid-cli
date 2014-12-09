# -*- coding: utf-8 -*-
import json

import click
import time
from druid_cli import tasks

from druid_cli.druid import DruidMixedAPI
from druid_cli.types import LOCATION, INTERVAL
from druid_cli.decorators import explain_errors

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
@click.option('-y', '--assume-yes', default=False, is_flag=True,
              help="Assume 'yes' on any interactive question")
@click.pass_context
def cli(ctx, overlord, coordinator, broker, assume_yes):
    ctx.obj = {
        'api': DruidMixedAPI(overlord, coordinator, broker),
        'assume_yes': assume_yes
    }


@cli.group(help="note: requires druid broker node")
def datasource():
    pass


@datasource.command(name="list", help="print all available datasources")
@click.pass_context
@explain_errors
def list_(ctx):
    api = ctx.obj['api']
    click.echo(json.dumps(api.get_datasources(), indent=INDENT))


@datasource.command(help="print details about given (or all) datasources")
@click.pass_context
@click.argument('datasources', nargs=-1)
@explain_errors
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
@explain_errors
def list_(ctx):
    api = ctx.obj['api']
    click.echo(json.dumps(api.get_servers(), indent=INDENT))


@server.command(help="print details of each server")
@click.pass_context
@click.argument('servers', nargs=-1)
@explain_errors
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


@server.command(help="print lists of segments in given (or all) servers")
@click.pass_context
@click.argument('servers', nargs=-1)
@explain_errors
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


@server.command(short_help="wait for epmty servers",
                help="Wait until there is no segments on given (or all) servers"
                     " or timeout uccured. druid-cli exits with 1 if timeout occured")
@click.pass_context
@click.option('--timeout',
              type=click.INT,
              default=None,
              help="wait timeout in seconds, 0 if no timeout (default)")
@click.argument('servers', nargs=-1)
@explain_errors
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
@explain_errors
def list_(ctx):
    api = ctx.obj['api']
    click.echo(json.dumps(api.get_rules(), indent=INDENT))


@cli.group(help="note: requires druid overlord node")
def task():
    pass


@task.command(name='list', help="print list of all tasks")
@click.pass_context
@explain_errors
def list_(ctx):
    api = ctx.obj['api']
    click.echo(json.dumps(api.get_tasks(), indent=INDENT))


@task.group(help="submit tasks to druid overlord")
def submit():
    pass


@submit.command(short_help="submit noop task",
                help="Submit noop task that does nothing. This is useful for testing.")
@click.pass_context
@explain_errors
def noop(ctx):
    api = ctx.obj['api']
    click.echo(
        json.dumps(api.post_task(tasks.NoopTask()), indent=INDENT)
    )



interval_argument = click.argument(
    'interval',
    type=INTERVAL,
    help="ISO formatted interval like 2010-10-10/2012-10-10 or one of those labels: {}".format(INTERVAL.ALL_TIME_LABELS)
)

@submit.command(short_help="submit kill task",
                help="Submit kill task that removes all "
                     "segments data for given datasources. "
                     "INTERVAL should be ISO formatted like: "
                     "2010-10-10/2012-10-10 or one of those "
                     "labels: {}. Use with caution!".format(INTERVAL.ALL_TIME_LABELS))
@click.pass_context
@click.argument('datasource',)
@click.argument('interval', type=INTERVAL)
@explain_errors
def kill(ctx, datasource, interval):
    api = ctx.obj['api']

    task_to_submit = tasks.KillTask(datasource, interval=interval)
    click.echo(
        json.dumps(api.post_task(task_to_submit), indent=INDENT)
    )


@submit.command(short_help="submit delete task",
                help="Submit detele task that creates empty segment with no data."
                     "INTERVAL should be ISO formatted like: "
                     "2010-10-10/2012-10-10 or one of those "
                     "labels: {}. Use with caution!".format(INTERVAL.ALL_TIME_LABELS))
@click.pass_context
@click.argument('datasource',)
@click.argument('interval', type=INTERVAL)
@explain_errors
def delete(ctx, datasource, interval):
    api = ctx.obj['api']
    task_to_submit = tasks.DeleteTask(datasource, interval=None)
    click.echo(
        json.dumps(api.post_task(task_to_submit), indent=INDENT)
    )
