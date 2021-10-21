from bson import ObjectId
from fastapi import HTTPException
from fastapi import status
from pymongo.collection import Collection

from common.consts import LATITUDE, LONGITUDE, COUNTRY, CITY, STREET, LOCATIONS
from routes.utils.locations import reverse_geo_location


def missing_param_exception(key):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'the {key} parameter is required')


class DataValidators:
    @staticmethod
    def locations(obj):
        if (
                obj.get('country')
                and obj.get('city')
                and obj.get('street')
                and not obj.get('latitude')
                and not obj.get('longitude')
        ):
            # we got strings repr of the location, let's try and fish its lat/long
            extra = reverse_geo_location(obj, from_latlon=False)
            obj[LATITUDE] = extra[0][LATITUDE]
            obj[LONGITUDE] = extra[0][LONGITUDE]
        elif (
                obj.get(LATITUDE)
                and obj.get(LONGITUDE)
                and not obj.get(COUNTRY)
                and not obj.get(CITY)
                and not obj.get(STREET)
        ):
            extra = reverse_geo_location(obj, from_latlon=True)
            obj[STREET], obj[CITY], obj[COUNTRY] = extra[0][STREET], extra[0][CITY], extra[0][COUNTRY]

        return obj

    @classmethod
    def get_d_type_validator(cls, d_type):
        d_types_to_funcs = {
            LOCATIONS: DataValidators.locations
        }
        return d_types_to_funcs[d_type]


class BaseUploaderFromAPI:
    """
    Describes uploading object with relations
    """
    collection: Collection = None
    id_field: str = None
    allowed_data_types: list = None

    def __init__(self, data, obj_id=None, new=True):
        self.initial_data = data
        if not obj_id and not new:
            raise ValueError('if you want to update a record, supply its id')
        self.obj_id = obj_id
        self.new = new

    async def upload(self):
        main_obj_id = self.serialize_input_for_upsert()
        for data_type in self.allowed_data_types:
            data = self.initial_data.get(data_type)
            await self._create_and_upload_related_data(data, inserted_id=main_obj_id, data_type=data_type)
        return main_obj_id

    async def _create_and_upload_related_data(self, data, inserted_id, data_type):
        inserted_id = inserted_id or self.obj_id
        validator_func = DataValidators.get_d_type_validator(d_type=data_type)
        validated_data = []
        for obj in data:
            obj[self.id_field] = ObjectId(inserted_id)
            validated_data.append(validator_func(obj))
        self.collection.insert_many(validated_data)

    def serialize_input_for_upsert(self) -> dict:
        raise NotImplemented

    def upsert_main_object(self, data):
        query = {'_id': ObjectId(self.obj_id)} if self.obj_id else data
        obj = self.collection.update_one(query, data, upsert=True)
        self.obj_id = obj.inserted_id
        return obj.inserted_id

    def log_meta(self, **kwargs):
        base = {
            'collection': self.collection.name,
        }
        if self.obj_id:
            base['object_id'] = self.obj_id
        base['mode'] = 'create' if self.new else 'update'
        base.update(**kwargs)
        return base
