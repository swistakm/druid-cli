# -*- coding: utf-8 -*-

from druid_cli.druid import DruidMixedAPI

api = DruidMixedAPI(
    broker_url='http://localhost:8080',
    coordinator_url='http://localhost:8082',
    overlord_url='http://localhost:8084'
)


def test_get_datasources():
    datasources = api.get_datasources()
    assert datasources


def test_get_datasource():
    datasources = api.get_datasources()
    first_datasource = api.get_datasource(datasources[0])
    assert first_datasource


def test_get_datasource_metrics():
    datasources = api.get_datasources()
    metrics = api.get_datasource_metrics(datasources[0])
    assert metrics


def test_get_datasource_dimensions():
    datasources = api.get_datasources()
    dimensions = api.get_datasource_dimensions(datasources[0])
    assert dimensions


def test_get_servers():
    servers = api.get_servers()
    assert servers


def test_get_server():
    servers = api.get_servers()
    first_server = api.get_server(servers[0])
    assert first_server


def test_get_server_segments():
    servers = api.get_servers()
    first_server = api.get_server_segments(servers[0])
    assert first_server


def test_get_rules():
    rules = api.get_rules()
    assert rules