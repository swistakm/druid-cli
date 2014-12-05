# -*- coding: utf-8 -*-
import functools

import click

from druid_cli import errors


def explain_errors(fun):
    @functools.wraps(fun)
    def wrapped(*args, **kwargs):
        try:
            fun(*args, **kwargs)
        except errors.DruidApiEndpointException, err:
            click.echo(err.get_request_error_message())

    return wrapped