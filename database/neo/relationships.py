from uuid import uuid4

from neomodel import (StructuredNode, Relationship, StringProperty,
                      DateTimeProperty, RelationshipTo, StructuredRel, UniqueIdProperty,
                      )
from neomodel.contrib.spatial_properties import NeomodelPoint


class DefaultMixin:
    id = UniqueIdProperty()
    date_added = DateTimeProperty()


class CompanyIndustries(StructuredRel, DefaultMixin):
    pass


class CompanyLocations(StructuredRel, DefaultMixin):
    type = StringProperty()


class Industry(StructuredNode, DefaultMixin):
    StringProperty(unique_index=True, default=uuid4)
    name = StringProperty(required=True)


class Location(StructuredNode, DefaultMixin):
    type = StringProperty()
    latitude = NeomodelPoint(**dict(crs='wgs84'))


class Company(StructuredNode, DefaultMixin):
    name = StringProperty(required=True)
    industries = RelationshipTo('Industry', "COMPANY_INDUSTRIES", model=CompanyIndustries)
    locations = Relationship('Location', "COMPANY_LOCATIONS", model=CompanyLocations)
