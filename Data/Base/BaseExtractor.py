from Data.Base.BaseDataClass import BaseDataProcess


class BaseExtractor(BaseDataProcess):
    @classmethod
    def extract(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def call_api(cls, *args, **kwargs):
        raise NotImplementedError
