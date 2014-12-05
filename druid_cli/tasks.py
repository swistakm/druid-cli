# -*- coding: utf-8 -*-
import json


class BaseTask(object):
    task_type = None
    _required_attrs = []

    def __init__(self, datasource=None, segments=None):
        self.segments = segments
        self.datasource = datasource
        self._check_required_attrs()

    def get_payload(self, **kwargs):
        """ Return payload added to task definition
        """
        payload = {
            'type': self.task_type,
            'dataSource': self.datasource
        }
        if self.segments:
            payload['segments'] = self.segments

        payload.update(kwargs)
        return payload

    def _check_required_attrs(self):
        for field in self._required_attrs:
            if getattr(self, field) is None:
                raise ValueError(
                    "%s field can not be %s" % (field, getattr(self, field))
                )

    def as_json(self):
        """ Return task definition as json string
        """
        return json.dumps(self.get_payload())


class BaseIntervalTask(BaseTask):
    def __init__(self, datasource=None, segments=None, interval=None):
        self.interval = interval
        super(BaseIntervalTask, self).__init__(datasource, segments)

    def get_iso_interval(self):
        # no interval given so we assume that task should be run for 'ever' interval
        if not self.interval:
            # not beautiful but is quite common practice
            return '0000-01-01/9999-12-31'

        start, end = self.interval

        return "{start}/{end}".format(start=start.isoformat(), end=end.isoformat())

    def get_payload(self, **kwargs):
        return super(BaseIntervalTask, self).get_payload(
            interval=self.get_iso_interval(),
            **kwargs
        )


class NoopTask(BaseIntervalTask):
    task_type = 'noop'

    def __init__(self, datasource=None, segments=None, interval=None, run_time=None, firehose=None):
        self.run_time = run_time
        self.firehose = firehose
        super(NoopTask, self).__init__(datasource, segments, interval)

    def get_payload(self, **kwargs):
        if self.run_time:
            kwargs['runTime'] = self.run_time

        if self.firehose:
            kwargs['firehose'] = self.firehose

        return super(NoopTask, self).get_payload(**kwargs)


class KillTask(BaseIntervalTask):
    task_type = 'kill'
    # _required_attrs = ['datasource']


class DeleteTask(BaseIntervalTask):
    task_type = 'delete'
    _required_attrs = ['datasource']


class MergeTask(BaseIntervalTask):
    task_type = 'merge'
    _required_attrs = ['datasource']


class AppendTask(BaseIntervalTask):
    task_type = 'append'
    _required_attrs = ['datasource']
