# -*- coding: utf-8 -*-
import click


class LocationUrlType(click.ParamType):
    name = 'location'

    def convert(self, value, param, ctx):
        if not (value.startswith('http://') or value.startswith("https://")):
            return 'http://' + value
        return value


LOCATION = LocationUrlType()
