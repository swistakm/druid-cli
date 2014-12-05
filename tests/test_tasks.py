# -*- coding: utf-8 -*-
import json
import datetime
import pytest

from druid_cli import tasks

DEFAULT_DATASOURCE = 'testdtasource'
DEFAULT_SEGMENTS = ['a', 'b']


def test_task_required_attrs():
    class DataSourceRequiredTask(tasks.BaseTask):
        _required_attrs = ['datasource']

    with pytest.raises(ValueError):
        DataSourceRequiredTask()

    assert DataSourceRequiredTask(datasource=DEFAULT_DATASOURCE)


def test_base_task_json():
    # test with segments
    task = tasks.BaseTask(datasource=DEFAULT_DATASOURCE, segments=DEFAULT_SEGMENTS)

    payload = json.loads(task.as_json())

    assert payload == {
        'type': None,
        'dataSource': DEFAULT_DATASOURCE,
        'segments': DEFAULT_SEGMENTS,
    }

    # and without segments
    task = tasks.BaseTask(datasource=DEFAULT_DATASOURCE,)

    payload = json.loads(task.as_json())

    assert payload == {
        'type': None,
        'dataSource': DEFAULT_DATASOURCE
    }


def test_base_interval_task_json():
    # test with infinite period
    task = tasks.BaseIntervalTask(datasource=DEFAULT_DATASOURCE)

    payload = json.loads(task.as_json())

    assert payload == {
        'type': None,
        'dataSource': DEFAULT_DATASOURCE,
        'interval': '0000-01-01/9999-12-31'
    }

    # and explicit period
    start = datetime.date(2001, 01, 01)
    end = datetime.date(2010, 01, 01)
    task = tasks.BaseIntervalTask(datasource=DEFAULT_DATASOURCE, interval=(start, end))
    payload = json.loads(task.as_json())

    assert payload == {
        'type': None,
        'dataSource': DEFAULT_DATASOURCE,
        'interval': '2001-01-01/2010-01-01'
    }


def test_noop_task_json():
    # test with infinite period
    start = datetime.date(2001, 01, 01)
    end = datetime.date(2010, 01, 01)

    task = tasks.NoopTask(datasource=DEFAULT_DATASOURCE, interval=(start, end))
    payload = json.loads(task.as_json())

    assert payload == {
        'type': 'noop',
        'dataSource': DEFAULT_DATASOURCE,
        'interval': '2001-01-01/2010-01-01'
    }


def test_kill_task_json():
    # test with infinite period
    start = datetime.date(2001, 01, 01)
    end = datetime.date(2010, 01, 01)

    task = tasks.KillTask(datasource=DEFAULT_DATASOURCE, interval=(start, end))
    payload = json.loads(task.as_json())

    assert payload == {
        'type': 'kill',
        'dataSource': DEFAULT_DATASOURCE,
        'interval': '2001-01-01/2010-01-01'
    }


def test_delete_task_json():
    # test with infinite period
    start = datetime.date(2001, 01, 01)
    end = datetime.date(2010, 01, 01)

    task = tasks.DeleteTask(datasource=DEFAULT_DATASOURCE, interval=(start, end))
    payload = json.loads(task.as_json())

    assert payload == {
        'type': 'delete',
        'dataSource': DEFAULT_DATASOURCE,
        'interval': '2001-01-01/2010-01-01'
    }


def test_append_task_json():
    # test with infinite period
    start = datetime.date(2001, 01, 01)
    end = datetime.date(2010, 01, 01)

    task = tasks.AppendTask(datasource=DEFAULT_DATASOURCE, interval=(start, end))
    payload = json.loads(task.as_json())

    assert payload == {
        'type': 'append',
        'dataSource': DEFAULT_DATASOURCE,
        'interval': '2001-01-01/2010-01-01'
    }


def test_merge_task_json():
    # test with infinite period
    start = datetime.date(2001, 01, 01)
    end = datetime.date(2010, 01, 01)

    task = tasks.MergeTask(datasource=DEFAULT_DATASOURCE, interval=(start, end))
    payload = json.loads(task.as_json())

    assert payload == {
        'type': 'merge',
        'dataSource': DEFAULT_DATASOURCE,
        'interval': '2001-01-01/2010-01-01'
    }