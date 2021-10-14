from Data.Base.BaseExtractor import BaseExtractor
from Data.Registry import extractor


@extractor
class ResearchExtractor(BaseExtractor):
    @classmethod
    def extract(cls, *args, **kwargs):
        pass