import requests

from ccl.api_utils.handlers.base import BaseAPIHandler
from common.consts import EMISSIONS
from common.data_providers import APIsURLs, Providers




class CitiesDataSearchHandler:

    def make_api_request(self, data_type):
        if data_type == EMISSIONS:
            urls = APIsURLs.get_urls(provider_or_providers=Providers.EMISSIONS_PROVIDERS)
        else:
            urls = []
        if isinstance(urls, str):
            urls = [urls]

        for url in urls:
            resp = requests.get(url=url)

    def city(self, *args, **kwargs):
        pass

