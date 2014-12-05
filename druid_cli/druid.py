# -*- coding: utf-8 -*-
import urlparse

import requests

from druid_cli import errors


class DruidEndpoint(object):
    endpoint_path = None

    def __init__(self, url=None, endpoint_path=""):
        self.endpoint_path = endpoint_path
        self.base_url = urlparse.urljoin(url, self.endpoint_path)

    def get(self, resource, **params):
        resource_url = urlparse.urljoin(self.base_url, resource)
        response = requests.get(resource_url, **params)
        self._raise_for_status(response)
        return response

    def post(self, resource, **params):
        resource_url = urlparse.urljoin(self.base_url, resource)
        response = requests.post(resource_url, **params)
        self._raise_for_status(response)
        return response

    def delete(self, resource, **params):
        resource_url = urlparse.urljoin(self.base_url, resource)
        response = requests.delete(resource_url, **params)
        self._raise_for_status(response)
        return response

    def put(self, resource, **params):
        resource_url = urlparse.urljoin(self.base_url, resource)
        response = requests.put(resource_url, **params)
        self._raise_for_status(response)
        return response

    def _raise_for_status(self, response):
        """ Check if response has valid status code and raise specific druid-cli
        exception

        :param response: Druid http response object
        :type response: requests.Response
        :return: None
        """
        try:
            response.raise_for_status()
        except requests.HTTPError, err:
            raise errors.DruidApiEndpointException(err.message, response)


class DruidMixedAPI(object):
    DEFAULT_OVERLORD_URL = 'http://localhost:8080'
    DEFAULT_COORDINATOR_URL = 'http://localhost:8080'
    DEFAULT_BROKER_URL = 'http://localhost:8080'

    def __init__(self, overlord_url=None, coordinator_url=None, broker_url=None):
        self.overlord_url = overlord_url or self.DEFAULT_OVERLORD_URL
        self.coordinator_url = coordinator_url or self.DEFAULT_COORDINATOR_URL
        self.broker_url = broker_url or self.DEFAULT_BROKER_URL

        self.overlord = DruidEndpoint(self.overlord_url, 'druid/v2/')
        self.indexer = DruidEndpoint(self.overlord_url, 'druid/indexer/v1/')
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

    def get_tasks(self):
        return {
            "running": self.indexer.get('runningTasks').json(),
            "pending": self.indexer.get('pendingTasks').json(),
            "waiting": self.indexer.get('waitingTasks').json(),
            "complete": self.indexer.get('completeTasks').json(),
        }

    def post_task(self, task):
        return self.indexer.post(
            'task',
            data=task.as_json(),
            headers={'content-type': 'application/json'}
        ).json()
