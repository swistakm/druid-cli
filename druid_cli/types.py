# -*- coding: utf-8 -*-
import click
import datetime
import dateutil.parser


class LocationUrlType(click.ParamType):
    name = 'location'

    def convert(self, value, param, ctx):
        if not (value.startswith('http://') or value.startswith("https://")):
            return 'http://' + value
        return value


class Interval(click.ParamType):
    name = 'interval'
    ALL_TIME_LABELS = ('@all', '@ever')

    def convert(self, value, param, ctx):
        try:
            interval = self.parse_interval_value(value)
        except ValueError:
            self.fail(
                "{} is not a valid interval specifier. "
                "Use something like 2010-10-10/2012-10-19 or one of those labels: "
                "{}".format(value, self.ALL_TIME_LABELS)
            )

        self.confirm_interval(interval, ctx)
        return interval

    def parse_interval_value(self, value):
        if value in self.ALL_TIME_LABELS:
            interval = datetime.datetime(1, 1, 1), datetime.datetime(9999, 12, 31)
        else:
            start, end = value.split('/')
            interval = dateutil.parser.parse(start), dateutil.parser.parse(end)

        return interval

    def confirm_interval(self, interval, ctx):
        if ctx.obj.get('assume_yes'):
            return

        for time in interval:
            if time - datetime.datetime.utcnow() > datetime.timedelta():
                answer = click.confirm(
                    "[{}] is a future time. Are you sure what you are doing?".format(time)
                )
                if not answer:
                    ctx.fail("Aborted")

INTERVAL = Interval()
LOCATION = LocationUrlType()
