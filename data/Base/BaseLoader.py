from Data.Base.BaseDataClass import BaseDataProcess


class BaseLoader(BaseDataProcess):

    def __init__(self, transformed_data):
        super().__init__()
        self.transformed_data = transformed_data

    def validate_data(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def load(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def is_data_validated(self) -> bool:
        validated = self.validate_data()
        return validated
