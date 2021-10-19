from typing import Optional

import requests

from data.base.base_data_class import BaseDataProcess


class BaseExtractor(BaseDataProcess):
    @classmethod
    def extract(cls, *args, **kwargs):
        raise NotImplementedError


class BaseAPIExtractor(BaseExtractor):
    def get_headers(self):
        return {}

    def get_url(self):
        raise NotImplementedError

    def get_url_params(self, params: Optional[dict] = None):
        raise NotImplementedError

    def get_request_body(self, data: Optional[dict] = None):
        return

    def handle_call_response(self, response):
        """
        this method parses the api response data or raise errors and logs if needed
        """
        raise NotImplementedError

    def make_api_call(self, url_params: Optional[dict] = None, body_params: Optional[dict] = None):
        url = self.get_url()
        headers = self.get_headers()
        body = self.get_request_body(body_params)
        params = self.get_url_params(url_params)
        resp = requests.get(url=url, headers=headers, params=params, data=body)
        return resp
