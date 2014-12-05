# -*- coding: utf-8 -*-
import re

import html2text
import requests

html_handler = html2text.HTML2Text()


class BaseDruidCliException(Exception):
    """ Base exception for all druid-cli exceptions"""


class DruidApiEndpointException(BaseDruidCliException):
    """ Represents exceptions raised by querying druid API endpoint"""
    def __init__(self, msg, response=None):
        """
        :param msg:
        :param response:
        :type response: requests.Response
        :return:
        """
        self.response = response
        super(DruidApiEndpointException, self).__init__(msg)

    def _format_html_content(self):
        content = html_handler.handle(self.response.content)
        # get rid of first header
        content = re.sub(r"##.+\n", '', content, count=1)
        # get rid of jetty footer
        content = re.sub(r"_Powered by Jetty://_\n", '', content)
        # het rid of hr
        content = re.sub(r"\* \* \*\n", '', content)
        # get rid of excessive empty lines
        content = re.sub(r"\n\s+\n", '\n', content)
        return content

    def get_request_error_message(self):
        return (
            "Druid endpoint {url} responded with status code <{code}>:\n"
            "{content}\n"
            "---\n"
            "Hint: {hint}\n"
        ).format(
            url=self.response.url,
            code=self.response.status_code,
            content=self._format_html_content(),
            hint= self.get_hint()
        )

    def get_hint(self):
        if self.response.status_code == 404:
            return "check if you have set broker/coordinator/overlord locations properly"

        return "no hint for you available"


