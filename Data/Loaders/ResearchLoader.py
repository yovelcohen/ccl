from Data.Base.BaseLoader import BaseLoader
from Data.Registry import loader
from consts import QUESTIONABLE_SOURCES

ALLOWED_QUESTIONABLE_SOURCES = 3


@loader
class ResearchLoader(BaseLoader):
    def validate_data(self) -> bool:
        if (
                not self.transformed_data
                or
                not self._source_validation()
        ):
            return False
        else:
            return True

    def _source_validation(self):
        sources = self.transformed_data['sources'].uniuqe().tolist()
        intersect = set(sources).intersection(QUESTIONABLE_SOURCES)
        if len(intersect) > ALLOWED_QUESTIONABLE_SOURCES:
            return False
        return True
