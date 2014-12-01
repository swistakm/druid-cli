# -*- coding: utf-8 -*-
import urlparse

import requests


class DruidEndpoint(object):
    endpoint_path = None

    def __init__(self, url=None, endpoint_path=""):
        self.endpoint_path = endpoint_path
        self.base_url = urlparse.urljoin(url, self.endpoint_path)

    def get(self, resource, **payload):
        resource_url = urlparse.urljoin(self.base_url, resource)
        return requests.get(resource_url, params=payload)

    def post(self, resource, **payload):
        resource_url = urlparse.urljoin(self.base_url, resource)
        return requests.get(resource_url, params=payload)

    def delete(self, resource, **payload):
        resource_url = urlparse.urljoin(self.base_url, resource)
        return requests.get(resource_url, params=payload)

    def put(self, resource, **payload):
        resource_url = urlparse.urljoin(self.base_url, resource)
        return requests.get(resource_url, params=payload)


class DruidMixedAPI(object):
    DEFAULT_OVERLORD_URL = 'http://localhost:8080'
    DEFAULT_COORDINATOR_URL = 'http://localhost:8080'
    DEFAULT_BROKER_URL = 'http://localhost:8080'

    def __init__(self, overlord_url=None, coordinator_url=None, broker_url=None):
        self.overlord_url = overlord_url or self.DEFAULT_OVERLORD_URL
        self.coordinator_url = coordinator_url or self.DEFAULT_COORDINATOR_URL
        self.broker_url = broker_url or self.DEFAULT_BROKER_URL

        self.overlord = DruidEndpoint(self.overlord_url, 'druid/v2/')
        self.coordinator = DruidEndpoint(self.coordinator_url, 'druid/coordinator/v1/')
        self.broker = DruidEndpoint(self.broker_url, 'druid/v2/')

    def get_datasources(self):
        return self.broker.get(
            'datasources'
        ).json()

    def get_datasource(self, datasource_id):
        return self.broker.get(
            'datasources/{id}'.format(id=datasource_id)
        ).json()

    def get_datasource_metrics(self, datasource_id):
        return self.broker.get(
            'datasources/{id}/metrics'.format(id=datasource_id)
        ).json()

    def get_datasource_dimensions(self, datasource_id):
        return self.broker.get(
            'datasources/{id}/dimensions'.format(id=datasource_id)
        ).json()

    def get_servers(self):
        return self.coordinator.get(
            'servers'
        ).json()

    def get_server(self, server_id):
        return self.coordinator.get(
            'servers/{id}'.format(id=server_id)
        ).json()

    def get_server_segments(self, datasource_id):
        return self.coordinator.get(
            'servers/{id}/segments'.format(id=datasource_id)
        ).json()

    def get_rules(self):
        return self.coordinator.get(
            'rules'
        ).json()

