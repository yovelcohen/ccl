def _get_method(method):
    router = globals()['router']
    if method.lower() == 'get':
        return router.get
    elif method.lower() == 'post':
        return router.post
    elif method.lower() == 'put':
        return router.put
    elif method.lower() == 'delete':
        return router.delete


def register_endpoint(self, f, name, method='get'):
    """
    CBVs register ----- WIP
    """
    method = _get_method(method)

    @self.router(f'{self.tag}/{name}')
    def endpoint(*args, **kwargs):
        return f(*args, **kwargs)

    return endpoint
