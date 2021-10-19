from data.base.base_extractor import BaseAPIExtractor
from data.registry import extractor
from common.data_providers import APIsURLs, Providers


@extractor
class EndangeredAnimalsMetaDataExtractor(BaseAPIExtractor):
    flow = 'ENDANGERED_ANIMALS'

    def get_url(self):
        return APIsURLs.get_urls(Providers.BLOOWATCH)
