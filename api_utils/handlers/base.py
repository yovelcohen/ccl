import requests

from ccl.database.cybele.collections import pieces, locations, images


def authenticate_user(request) -> bool:
    pass


class BaseAPIHandler:
    tag = None
    router = None

    def __init__(self, request):
        self.request = request

    @property
    def is_authenticated(self):
        return authenticate_user(self.request)

    def create(self, data):
        """
        create new db record/s [POST]
        """
        raise NotImplemented

    def update(self, data):
        """
        update exiting record [PUT/PATCH]
        """
        raise NotImplemented

    def get(self, *args, **kwargs):
        """
        filter and return records from db [GET]
        """
        raise NotImplemented

    def retrieve(self, **filters):
        """
        should return one record from db [GET]
        """
        raise NotImplemented

    def delete(self):
        """
        delete record/s from db [DELETE]
        """
        raise NotImplemented

    def models_to_collections(self):
        _map = {
            'POST': self.create,
            'PUT': self.update,
            'PATCH': self.update,
            'GET': self.get,
            'DELETE': self.delete
        }

    def make_api_request(self, *args, **kwargs):
        raise NotImplementedError
