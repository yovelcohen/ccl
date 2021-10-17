from data.Base.BaseExtractor import BaseAPIExtractor
from common.exceptions import APICallError
from data.registry import extractor


@extractor
class EmissionsAPIExtractor(BaseAPIExtractor):
    flow = 'EMISSIONS_API'

    def get_url(self):
        return 'https://api.v2.emissions-api.org/api/v2/'

    def get_url_params(self, params=None):
        data_type = params.pop('data_type', None)
        if not isinstance(data_type, str):
            raise KeyError("a data type must be supplied, one of methane, carbonmonoxide, ozone  must be provided")

    def handle_call_response(self, response):
        data = response.json()
        status_code = response.status
        if status_code != 200:
            raise APICallError('got error code')
