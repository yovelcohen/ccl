from functools import wraps

from fastapi import APIRouter

from api_utils.handlers.base import BaseAPIHandler
from api_utils.handlers.location import LocationsHandler
from database.cybele.collections import locations

router = APIRouter()


def _handle_method(method):
    if method.lower() == 'get':
        return router.get


def register_endpoint(self, f, name, method='get'):
    method = _handle_method(method)

    @self.router(f'{self.tag}/{name}')
    def endpoint(*args, **kwargs):
        return f(*args, **kwargs)

    return endpoint()


class LocationsAPI(BaseAPIHandler):
    tag = '/location'
    router = router

    def search(self, *args, **kwargs):
        pass
