from uuid import uuid4

from neomodel import (StructuredNode, Relationship, StringProperty,
                      DateTimeProperty, RelationshipTo, NodeSet, DateProperty, One, FloatProperty
                      )
from neomodel.contrib.spatial_properties import NeomodelPoint
from pytz import country_names

from api_utils.exceptions import ValidationError
from common.consts import STREET, CITY, COUNTRY, LATITUDE, LONGITUDE
from common.utils import reverse_geo_location
from database.neo.relationships import CompanyLocations, CompanyIndustries, CompanyPieces


class DefaultMixin:
    date_added = DateTimeProperty()
    nodes: NodeSet  # makes pycharm smarter

    def exists(self, **filters) -> bool:
        """
        checks if a node of this filters exists
        """
        if not filters:
            if not self.id:
                raise KeyError('no filters or id provided')
            filters['id'] = self.id
        return bool(self.nodes.first_or_none(**filters))

    def related_exists(self, relation: str, **filters):
        relation_manager = getattr(self, relation, None)
        if not relation_manager:
            raise KeyError(f'{relation} not found!')
        return relation_manager.filter(**filters)


class Industry(StructuredNode, DefaultMixin):
    StringProperty(unique_index=True, default=uuid4)
    name = StringProperty(required=True)


class Location(StructuredNode, DefaultMixin):
    type = StringProperty()
    street = StringProperty()
    city = StringProperty()
    country = StringProperty(choices=country_names)

    latitude = FloatProperty()
    longitude = FloatProperty()
    geo_point = NeomodelPoint(**dict(crs='wgs84'))

    def save(self):
        base = {}
        if self.street:
            base[STREET] = self.street
        if self.city:
            base[CITY] = self.city
        if self.country:
            base[COUNTRY] = self.country
        if len(base) == 3:
            # alright, so we got all data for a location, if it exist in full form, why handle it?
            # if we don't got 3 filters so were updating and then it's okay?
            exists = self.nodes.first_or_none(**base)
            if exists:
                raise ValidationError('Location with this street, city, country already exists')

        if all(x is None for x in (self.latitude, self.longitude, self.street, self.city, self.country)):
            raise ValidationError("you didn't pass any parameters, WTF bruh?")

        # if only one of lat/long was provided
        if self.latitude and not self.longitude:
            raise ValidationError("you can't pass latitude without longitude")

        if self.longitude and not self.latitude:
            raise ValidationError("you can't pass longitude without latitude")

        # if only street and city, but no country
        if self.street and self.city and not self.country:
            raise ValidationError("come on, what can I do with street, city and not country")

        # done validation stuff, now let's fill missing data
        if self.has_full_address() and not self.has_point_or_lat_long():
            obj = dict(street=self.street,
                       city=self.city,
                       country=self.country)
            data = reverse_geo_location(obj)[0]
            self.latitude, self.longitude = data.get(LATITUDE), data.get(LONGITUDE)

        if self.latitude and self.longitude and not self.geo_point:
            self.geo_point = NeomodelPoint(**dict(latitude=self.latitude, longitude=self.longitude))
        super(Location, self).save()

    def has_full_address(self):
        return bool(self.street and self.city and self.country)

    def has_point_or_lat_long(self):
        return bool(self.latitude and self.longitude or self.geo_point)


class Company(StructuredNode, DefaultMixin):
    name = StringProperty(required=True)
    industries = RelationshipTo('Industry', "COMPANY_INDUSTRIES", model=CompanyIndustries)
    locations = Relationship('Location', "COMPANY_LOCATIONS", model=CompanyLocations)


class DataPiece(StructuredNode, DefaultMixin):  # noqa
    start_date = DateProperty()
    end_date = DateProperty()
    location = Relationship(Location, "PIECE_LOCATION", cardinality=One)
    industries = Relationship(Industry, "PIECE_INDUSTRIES")
    description = StringProperty()
    companies = Relationship(Company, "PIECE_COMPANIES", model=CompanyPieces)
