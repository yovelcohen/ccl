from data.Registry import load_cls


class ETLRunner:
    def __init__(self, flow, source):
        self._flow = flow
        self._source = source

    def extract_data(self):
        extractor_cls = load_cls(flow=self._flow, cls_type='extractors')
        return extractor_cls.extract()

    def transform_data(self, extracted_data):
        transformer_cls = load_cls(flow=self._flow, cls_type='transformers')
        transformed_data = transformer_cls(extracted_data=extracted_data).transformer()
        return transformed_data

    def load_data(self, transformed_data):
        loader_cls = load_cls(flow=self._flow, cls_type='loaders')
        loaded_data = loader_cls(transformed_data=transformed_data).load()
        return loaded_data

    @classmethod
    def run(cls, flow, source=None):
        self = cls(flow=flow, source=source)
        extracted_data = self.extract_data()
        transformed_data = self.transform_data(extracted_data=extracted_data)
        load_data = self.load_data(transformed_data=transformed_data)
        return load_data
