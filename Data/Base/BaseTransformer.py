import pandas as pd
from Data.Base.BaseDataClass import BaseDataProcess


class BaseTransformer(BaseDataProcess):
    def __init__(self, data):
        super().__init__()
        self.data: pd.DataFrame = data

    def transform(self):
        raise NotImplementedError
