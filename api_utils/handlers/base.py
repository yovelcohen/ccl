from ccl.database.cybele.collections import pieces, locations, images


def authenticate_user(request) -> bool:
    pass


class BaseAPIHandler:
    model = None

    def __init__(self, request):
        self.request = request

    @property
    def is_authenticated(self):
        return authenticate_user(self.request)

    def upload(self, data):
        raise NotImplemented

    def get(self, **filters):
        raise NotImplemented

    def delete(self):
        raise NotImplemented

    def update(self, data):
        raise NotImplemented

    def models_to_collections(self):
        _map = {
            'locations': locations,
            'images': images,
            'pieces': pieces
        }
        return _map[self.model]
