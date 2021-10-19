import pandas as pd
from data.base.base_data_class import BaseDataProcess


class BaseTransformer(BaseDataProcess):
    def __init__(self, data):
        super().__init__()
        self.data: pd.DataFrame = data

    def transform(self):
        raise NotImplementedError
